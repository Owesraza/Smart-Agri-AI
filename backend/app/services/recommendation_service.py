"""
Recommendation Service — Real-Time AI Intelligence Layer.
Combines Live Market Prices, Weather Analytics, EMA Trends, and FAISS RAG to produce:
- Structured Decision: SELL / WAIT / STORE
- Confidence Score (0-100%)
- Reason & Risk Level
- Suggested Market & Expected Price Trend
Stores recommendation in DB for tracking.
"""
import logging
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sql_models import RecommendationModel
from app.services.market_service import get_live_market_prices, compute_market_analytics, normalize_crop_name
from app.services.weather_service import get_current_weather
from app.ai.agents.farm_agent import run_ai_pipeline

logger = logging.getLogger(__name__)


async def generate_live_recommendation(
    db: AsyncSession,
    user_id: str,
    crop: str,
    location: str = "Nashik",
    harvest_date: Optional[str] = None,
    quantity: Optional[float] = None,
    user_question: Optional[str] = None,
) -> Dict:
    """
    Full Real-Time Intelligence Pipeline:
    1. Fetch live market prices & compute EMA/volatility
    2. Fetch live weather & harvest risk analytics
    3. Run AI Engine (Gemini 2.0 Flash + FAISS RAG)
    4. Save recommendation to `recommendations` table
    """
    crop_norm = normalize_crop_name(crop)

    # 1. Live Market Data & Analytics
    market_prices = await get_live_market_prices(db, crop=crop_norm, district=location)
    market_analytics = await compute_market_analytics(db, crop=crop_norm)

    current_price = market_analytics.get("today_avg_price") or (
        market_prices[0]["modal_price"] if market_prices else 2200.0
    )

    # Historical price series for EMA
    historical_series = [p["modal_price"] for p in market_prices[::-1]] if market_prices else [current_price]

    # 2. Live Weather Data
    weather = await get_current_weather(db, location=location)

    # 3. Formulate Question for AI Agent
    question = user_question or (
        f"Should I sell my {crop_norm} harvest now at ₹{current_price}/quintal in {location}, "
        f"or store it? Consider current weather ({weather.get('condition')}, {weather.get('harvest_risk')} harvest risk) "
        f"and market trend ({market_analytics.get('market_trend')})."
    )

    # 4. Execute AI Pipeline (FAISS RAG + Gemini 2.0 Flash + Rule-engine fallback)
    ai_result = await run_ai_pipeline(
        question=question,
        crop=crop_norm,
        location=location,
        current_price=current_price,
        historical_prices=historical_series,
    )

    recommendation = ai_result.get("recommendation", "WAIT")
    confidence = ai_result.get("confidence", 60)
    reason = ai_result.get("reason") or ai_result.get("answer", "Analysis complete based on market trend and weather.")
    risk_level = weather.get("harvest_risk", "Low")
    suggested_market = market_prices[0]["mandi"] if market_prices else f"{location} APMC"
    expected_trend = ai_result.get("expected_price_trend") or market_analytics.get("market_trend", "STABLE")

    # 5. Save to `recommendations` database table
    try:
        rec_obj = RecommendationModel(
            user_id=user_id,
            crop=crop_norm,
            recommendation=recommendation,
            confidence=float(confidence),
            reason=reason[:500],
            risk_level=risk_level,
            suggested_market=suggested_market,
            expected_price_trend=expected_trend,
        )
        db.add(rec_obj)
        await db.commit()
    except Exception as e:
        logger.warning(f"Failed to save recommendation to DB: {e}")

    logger.info(f"💡 Real-Time Recommendation: {recommendation} ({confidence}%) for {crop_norm} @ ₹{current_price}")

    return {
        "crop": crop_norm,
        "recommendation": recommendation,
        "confidence": confidence,
        "current_price": current_price,
        "reason": reason,
        "risk_level": risk_level,
        "suggested_market": suggested_market,
        "expected_price_trend": expected_trend,
        "market_analytics": market_analytics,
        "weather": {
            "temperature": weather.get("temperature"),
            "condition": weather.get("condition"),
            "rain_probability": weather.get("rain_probability"),
            "rain_risk": weather.get("rain_risk"),
            "harvest_risk": weather.get("harvest_risk"),
            "advisory": weather.get("farming_advisory"),
        },
        "workflow": ai_result.get("workflow", []),
        "references": ai_result.get("references", []),
    }


async def get_user_recommendations(db: AsyncSession, user_id: str, limit: int = 10) -> List[Dict]:
    """Retrieve stored historical recommendations for a user."""
    stmt = (
        select(RecommendationModel)
        .where(RecommendationModel.user_id == user_id)
        .order_by(RecommendationModel.created_at.desc())
        .limit(limit)
    )
    res = await db.execute(stmt)
    recs = res.scalars().all()
    return [
        {
            "id": r.id,
            "crop": r.crop,
            "recommendation": r.recommendation,
            "confidence": r.confidence,
            "reason": r.reason,
            "risk_level": r.risk_level,
            "suggested_market": r.suggested_market,
            "expected_price_trend": r.expected_price_trend,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in recs
    ]
