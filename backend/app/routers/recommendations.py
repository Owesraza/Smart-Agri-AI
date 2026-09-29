"""Recommendations router — /api/v1/recommendations"""
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel, Field

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import recommendation_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/recommendations", tags=["AI Recommendations"])


class RecommendationRequest(BaseModel):
    crop: str = Field(..., description="Crop name e.g. Wheat, Onion")
    location: Optional[str] = Field(default="Nashik", description="Farmer location/district")
    harvest_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    quantity: Optional[float] = Field(default=None, gt=0, description="Quantity in quintals")
    user_question: Optional[str] = Field(default=None, description="Specific question")


@router.post("/generate", summary="Generate real-time AI recommendation (SELL / WAIT / STORE)")
async def generate_recommendation(
    data: RecommendationRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate structured real-time AI recommendation combining:
    - Live Agmarknet mandi market prices & EMA trends
    - Live OpenWeatherMap weather & harvest risk analytics
    - Gemini 2.0 Flash + FAISS RAG agricultural knowledge
    """
    result = await recommendation_service.generate_live_recommendation(
        db=db,
        user_id=current_user["id"],
        crop=data.crop,
        location=data.location or current_user.get("district", "Nashik"),
        harvest_date=data.harvest_date,
        quantity=data.quantity,
        user_question=data.user_question,
    )
    return success_response(result, f"Recommendation generated for {data.crop}")


@router.get("/smart-price", summary="Get multi-factor AI price recommendation for farmer/buyer")
async def get_smart_price(
    crop: str = Query("Onion", description="Crop name"),
    district: Optional[str] = Query("Nashik", description="District/location"),
    quantity: Optional[float] = Query(100.0, ge=0),
    quality_grade: Optional[str] = Query("Grade A"),
    role: Optional[str] = Query("farmer", description="farmer or buyer"),
    user_price: Optional[float] = Query(None, description="Current listing/offered price"),
    language: Optional[str] = Query("English", description="Response language"),
    db: AsyncSession = Depends(get_db),
):
    from app.services.recommend_price_service import get_smart_price_recommendation
    result = await get_smart_price_recommendation(
        db=db,
        crop=crop,
        district=district,
        quantity=quantity,
        quality_grade=quality_grade,
        role=role,
        user_price=user_price,
        language=language,
    )
    return success_response(result, f"Smart price recommendation generated for {crop}")


@router.get("/", summary="Get user's past recommendations")
@router.get("", summary="Get user's past recommendations")
async def list_recommendations(
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    history = await recommendation_service.get_user_recommendations(
        db=db,
        user_id=current_user["id"],
        limit=limit,
    )
    return success_response(history, "Past recommendations fetched")
