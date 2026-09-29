"""AI Router — /api/v1/ai"""
import time
import logging
from fastapi import APIRouter, Depends, Body, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.ai import ai_service
from app.services.recommend_price_service import get_smart_price_recommendation
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/ai", tags=["AI Engine"])
logger = logging.getLogger(__name__)


# ── Request Schemas ────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="Farmer's question")
    crop: Optional[str] = Field(default="General", description="Crop being asked about")
    location: Optional[str] = Field(default="India", description="Farmer's location")
    current_price: Optional[float] = Field(default=None, gt=0, description="Current mandi price per quintal")
    historical_prices: Optional[List[float]] = Field(default=None, description="List of past prices (oldest→newest)")
    language: Optional[str] = Field(default="English", description="Preferred language for response")


class ProfitAnalysisRequest(BaseModel):
    ledger_entries: List[dict] = Field(..., description="Array of ledger entry objects")
    crop: Optional[str] = Field(default=None)


class WorkflowRequest(BaseModel):
    crop: str = Field(..., description="Crop name")
    harvest_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    quantity: Optional[float] = Field(default=None, gt=0, description="Quantity in quintals")
    mandi: Optional[str] = Field(default=None)
    recommendation: Optional[str] = Field(default="SELL")


class TrendRequest(BaseModel):
    prices: List[float] = Field(..., min_length=3, description="Price series (oldest→newest)")


class PriceRecommendRequest(BaseModel):
    crop: str = Field(..., example="Wheat")
    district: Optional[str] = Field(default="Nashik")
    quantity: Optional[float] = Field(default=100.0)
    quality: Optional[str] = Field(default="Grade A")
    quality_grade: Optional[str] = Field(default="Grade A")
    role: Optional[str] = Field(default="farmer")
    user_price: Optional[float] = Field(default=None)
    language: Optional[str] = Field(default="English")


# ── Endpoints ──────────────────────────────────────────────
@router.post("/recommend-price", summary="Get AI Smart Price Recommendation for Farmers/Buyers")
async def recommend_price_endpoint(
    data: PriceRecommendRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await get_smart_price_recommendation(
        db=db,
        crop=data.crop,
        district=data.district,
        quantity=data.quantity,
        quality_grade=data.quality_grade or data.quality,
        role=data.role or "farmer",
        user_price=data.user_price,
        language=data.language or "English",
    )
    return success_response(result, "AI Smart Price Recommendation generated")


@router.get("/status", summary="Check AI engine readiness")
async def ai_status():
    ready = ai_service.is_ai_ready()
    return success_response(
        {"ready": ready, "status": "ONLINE" if ready else "INITIALIZING"},
        "AI Engine status"
    )


@router.post("/chat", summary="Main AI chat endpoint (POST /chat)")
@router.post("/ask", summary="Main AI chat endpoint alias (POST /ask)")
async def ai_chat(
    data: ChatRequest,
    current_user: dict = Depends(get_current_active_user),
):
    """
    Full AI pipeline:
    - Intent detection
    - RAG retrieval from agricultural knowledge base
    - EMA market trend analysis
    - Rule-based SELL/WAIT/STORE recommendation
    - Gemini 2.5 Flash explanation
    - Workflow generation
    - Confidence scoring
    """
    logger.info(
        f"[/ai/chat] user={current_user['id']} crop={data.crop} "
        f"price={data.current_price} q='{data.question[:50]}'"
    )

    result = await ai_service.chat(
        question=data.question,
        crop=data.crop or "General",
        location=data.location or current_user.get("district", "India"),
        current_price=data.current_price,
        historical_prices=data.historical_prices,
        language=data.language,
        user_id=current_user["id"],
    )
    return success_response(result, "AI response generated")


@router.post("/recommend", summary="Get SELL/WAIT/STORE recommendation for a crop")
async def get_recommendation(
    crop: str = Query(...),
    current_price: float = Query(..., gt=0),
    historical_prices: Optional[str] = Query(None, description="Comma-separated prices, oldest first"),
    current_user: dict = Depends(get_current_active_user),
):
    """Quick recommendation without full chat — for dashboard widget."""
    from app.ai.forecasting.ema import analyze_trend
    from app.ai.recommendation.engine import generate_recommendation

    prices = []
    if historical_prices:
        try:
            prices = [float(p.strip()) for p in historical_prices.split(",")]
        except ValueError:
            prices = []

    trend_data = analyze_trend(prices) if prices else {"trend": "UNKNOWN", "confidence": 0}
    rec = generate_recommendation(
        crop=crop,
        current_price=current_price,
        trend_data=trend_data,
        historical_prices=prices,
    )
    return success_response(rec, f"Recommendation for {crop}")


@router.post("/profit-analysis", summary="Analyze ledger data for profit insights")
async def profit_analysis(
    data: ProfitAnalysisRequest,
    current_user: dict = Depends(get_current_active_user),
):
    result = await ai_service.analyze_profit_data(data.ledger_entries, data.crop)
    return success_response(result, "Profit analysis complete")


@router.post("/workflow", summary="Generate harvest-to-sale workflow")
async def create_workflow(
    data: WorkflowRequest,
    current_user: dict = Depends(get_current_active_user),
):
    workflow = await ai_service.get_workflow(
        crop=data.crop,
        harvest_date=data.harvest_date,
        quantity=data.quantity,
        mandi=data.mandi or current_user.get("district", "Nearest APMC"),
        recommendation=data.recommendation or "SELL",
    )
    return success_response(workflow, f"Workflow generated for {data.crop}")


@router.post("/trend", summary="EMA trend analysis on price series")
async def market_trend(
    data: TrendRequest,
    current_user: dict = Depends(get_current_active_user),
):
    result = await ai_service.get_market_trend(data.prices)
    return success_response(result, "Trend analysis complete")


@router.get("/intent", summary="Detect intent from a question")
async def detect_intent_endpoint(
    question: str = Query(..., min_length=3),
    current_user: dict = Depends(get_current_active_user),
):
    from app.ai.utils.intent_detector import detect_intent
    result = detect_intent(question)
    return success_response(result, "Intent detected")
