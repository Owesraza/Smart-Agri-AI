"""Buyer router — /api/v1/buyer"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import buyer_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/buyer", tags=["Buyer Management"])


class BuyerRegistrationRequest(BaseModel):
    full_name: str = Field(..., example="Amit Traders")
    mobile_number: str = Field(..., example="9876500000")
    email: str = Field(..., example="amit@traders.com")
    password: str = Field(..., example="Password123!")
    company_name: str = Field(..., example="Amit Agri Traders Pvt Ltd")
    owner_name: str = Field(..., example="Amit Sharma")
    gst_number: Optional[str] = Field(default="27AAACA1234A1Z5")
    business_license: Optional[str] = Field(default="APMC-NSK-992")
    address: Optional[str] = Field(default="Market Yard, Nashik")
    district: str = Field(default="Nashik")
    state: str = Field(default="Maharashtra")
    pincode: Optional[str] = Field(default="422001")
    buying_crops: Optional[str] = Field(default="Wheat, Onion, Tomato")
    daily_capacity: Optional[float] = Field(default=200.0)
    preferred_payment_time: Optional[str] = Field(default="Immediate")


@router.post("/register", summary="Register a new Buyer account")
async def register_buyer_endpoint(data: BuyerRegistrationRequest, db: AsyncSession = Depends(get_db)):
    user_payload = {
        "full_name": data.full_name,
        "mobile_number": data.mobile_number,
        "email": data.email,
        "password": data.password,
        "village": data.address,
    }
    profile_payload = data.model_dump()
    result = await buyer_service.register_buyer(db, user_payload, profile_payload)
    return success_response(result, "Buyer account registered successfully")


@router.get("/list", summary="List all real registered buyers")
async def list_buyers_endpoint(db: AsyncSession = Depends(get_db)):
    buyers = await buyer_service.list_buyers(db)
    return success_response(buyers, f"{len(buyers)} registered buyers fetched")


@router.get("/dashboard", summary="Get Buyer Dashboard KPIs & Metrics")
async def buyer_dashboard_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stats = await buyer_service.get_buyer_dashboard(db, current_user["id"])
    return success_response(stats, "Buyer dashboard metrics fetched")
