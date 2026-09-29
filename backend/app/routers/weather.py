"""Weather router — /api/v1/weather (live OpenWeatherMap API)"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.services import weather_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])


@router.get("/", summary="Get current weather (root endpoint)")
@router.get("/current", summary="Get live current weather & agricultural risk analytics")
async def get_current_weather_api(
    location: Optional[str] = Query(None, description="City/District name e.g. Nashik, Pune"),
    district: Optional[str] = Query(None, description="District name"),
    city: Optional[str] = Query(None, description="City name"),
    db: AsyncSession = Depends(get_db),
):
    loc = location or district or city or "Nashik"
    weather = await weather_service.get_current_weather(db=db, location=loc)
    return success_response(weather, f"Current weather fetched for {loc}")


@router.get("/today", summary="Get today's weather")
async def today_weather(
    city: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    loc = city or location or "Nashik"
    weather = await weather_service.get_current_weather(db=db, location=loc)
    return success_response(weather, "Weather data fetched")


@router.get("/forecast", summary="Get 5-day weather forecast & rain probabilities")
async def weather_forecast(
    city: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    loc = city or location or "Nashik"
    weather = await weather_service.get_current_weather(db=db, location=loc)
    return success_response(
        {
            "location": loc,
            "forecast": weather.get("forecast", []),
            "rain_probability": weather.get("rain_probability", 0),
            "rain_risk": weather.get("rain_risk", "Low"),
            "harvest_risk": weather.get("harvest_risk", "Low"),
        },
        "Forecast fetched"
    )
