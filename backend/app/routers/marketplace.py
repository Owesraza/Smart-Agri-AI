"""Marketplace router — /api/v1/marketplace"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import marketplace_service, negotiation_assistant
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/marketplace", tags=["Agricultural Marketplace"])


class NegotiationRequest(BaseModel):
    crop: str = Field(..., description="Crop name e.g. Wheat")
    buyer_offered_price: float = Field(..., gt=0)
    farmer_expected_price: float = Field(..., gt=0)
    district: Optional[str] = Field(default="Nashik")


@router.get("/feed/farmer", summary="Get personalized Marketplace Feed for Farmers")
async def farmer_feed_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    feed = await marketplace_service.get_farmer_feed(db, current_user["id"])
    return success_response(feed, "Farmer feed fetched")


@router.get("/feed/buyer", summary="Get personalized Marketplace Feed for Buyers")
async def buyer_feed_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    feed = await marketplace_service.get_buyer_feed(db, current_user["id"])
    return success_response(feed, "Buyer feed fetched")


@router.get("/farmers/{id}", summary="Get Real Farmer Profile Details from Database")
async def get_farmer_profile_endpoint(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    profile = await marketplace_service.get_farmer_profile_by_id(db, id)
    return success_response(profile, "Farmer profile fetched from SQL database")


@router.get("/buyers/{id}", summary="Get Real Buyer Profile Details from Database")
async def get_buyer_profile_endpoint(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    profile = await marketplace_service.get_buyer_profile_by_id(db, id)
    return success_response(profile, "Buyer profile fetched from SQL database")


@router.post("/negotiate", summary="AI Negotiation Assistant guidance")
async def ai_negotiation_guidance(
    data: NegotiationRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    guidance = await negotiation_assistant.get_negotiation_guidance(
        db=db,
        crop=data.crop,
        buyer_offered_price=data.buyer_offered_price,
        farmer_expected_price=data.farmer_expected_price,
        district=data.district or current_user.get("district", "Nashik"),
    )
    return success_response(guidance, "AI negotiation advice generated")
