"""AI V2 Router — /api/v1/ai/v2 (Advanced AI, Crop Health, Forecasting, Geolocation)"""
from fastapi import APIRouter, Depends, Query, Body
from pydantic import BaseModel, Field
from typing import Optional
from app.dependencies.auth import get_current_active_user
from app.ai.crop_health import diagnose_crop_health
from app.ai.advanced_forecasting import generate_advanced_price_forecast, generate_crop_demand_forecast
from app.utils.geo import calculate_transport_metrics
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/ai/v2", tags=["Advanced AI & Forecasting V2"])


class CropHealthRequest(BaseModel):
    crop: str = Field(..., example="Wheat")
    symptom_keyword: Optional[str] = Field(default=None, example="yellow leaf rust")
    image_url: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default="English", example="Hindi")


@router.post("/crop-health", summary="AI Crop Health Diagnosis & Treatment")
async def crop_health_diagnosis_endpoint(
    data: CropHealthRequest,
    current_user: dict = Depends(get_current_active_user),
):
    result = await diagnose_crop_health(
        crop=data.crop,
        symptom_keyword=data.symptom_keyword,
        image_url=data.image_url,
        language=data.language or "English",
    )
    return success_response(result, f"Crop health diagnosis generated for {data.crop}")


@router.get("/forecast/advanced", summary="1, 3, 7, 15, 30-Day Advanced Price Forecast")
async def advanced_price_forecast_endpoint(
    crop: str = Query("Wheat"),
    current_price: float = Query(2300.0, gt=0),
    current_user: dict = Depends(get_current_active_user),
):
    result = generate_advanced_price_forecast(crop=crop, current_price=current_price)
    return success_response(result, f"Multi-horizon price forecast generated for {crop}")


@router.get("/forecast/demand", summary="AI Crop Demand & Export Forecasting")
async def crop_demand_forecast_endpoint(
    crop: str = Query("Wheat"),
    district: str = Query("Nashik"),
    current_user: dict = Depends(get_current_active_user),
):
    result = generate_crop_demand_forecast(crop=crop, district=district)
    return success_response(result, f"Demand forecast generated for {crop}")


@router.get("/geo/distance", summary="Calculate Geolocation Distance & Transport Time")
async def geo_distance_endpoint(
    origin: str = Query("Nashik"),
    destination: str = Query("Pune"),
    current_user: dict = Depends(get_current_active_user),
):
    result = calculate_transport_metrics(origin=origin, destination=destination)
    return success_response(result, f"Transport metrics calculated between {origin} and {destination}")
