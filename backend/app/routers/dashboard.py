"""Dashboard router — /api/v1/dashboard"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services.analytics_service import get_dashboard_stats
from app.services.market_service import get_live_market_prices
from app.services.weather_service import get_current_weather
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/live", summary="Get complete live dashboard payload (Weather, Market Prices, KPIs)")
async def live_dashboard(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns single consolidated live payload for Dashboard UI:
    - Current live weather & forecast
    - Live Agmarknet mandi market prices
    - KPI stats (total/active plots, pending tasks, net profit)
    - Last updated timestamp
    """
    user_loc = current_user.get("district") or current_user.get("village") or "Nashik"

    # Fetch live services
    stats = await get_dashboard_stats(db, current_user["id"])
    weather = await get_current_weather(db, location=user_loc)
    prices = await get_live_market_prices(db, district=user_loc)

    return success_response(
        {
            "user": {
                "id": current_user["id"],
                "name": current_user.get("full_name"),
                "role": current_user.get("role"),
                "location": f"{user_loc}, {current_user.get('state', 'Maharashtra')}".strip(", "),
            },
            "kpis": stats,
            "weather": weather,
            "market_prices": prices[:6],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "Live dashboard payload fetched"
    )


@router.get("/stats", summary="Get all dashboard KPIs in a single request")
async def dashboard_stats(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stats = await get_dashboard_stats(db, current_user["id"])
    return success_response(
        {
            "user": {
                "name": current_user.get("full_name"),
                "role": current_user.get("role"),
                "location": f"{current_user.get('district', '')}, {current_user.get('state', '')}".strip(", "),
            },
            "stats": stats,
        },
        "Dashboard data fetched"
    )
