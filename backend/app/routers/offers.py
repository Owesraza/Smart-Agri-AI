"""Offers router — /api/v1/offers"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import offer_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/offers", tags=["Offers & Negotiation"])


class OfferCreateRequest(BaseModel):
    listing_id: Optional[str] = Field(default=None)
    requirement_id: Optional[str] = Field(default=None)
    farmer_id: Optional[str] = Field(default=None)
    offered_price: float = Field(..., gt=0, example=2280.0)
    message: Optional[str] = Field(default="Offering ₹2,280/quintal for immediate pickup.")
    expected_pickup_date: Optional[date] = Field(default=None)


class CounterOfferRequest(BaseModel):
    counter_price: float = Field(..., gt=0, example=2310.0)
    message: Optional[str] = Field(default="Counter-offering ₹2,310/quintal.")


class RespondOfferRequest(BaseModel):
    accept: bool = Field(..., description="True to Accept, False to Reject")


@router.post("/", summary="Buyer or Farmer sends an offer", status_code=201)
async def make_offer(
    data: OfferCreateRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    offer = await offer_service.create_offer(db, current_user["id"], data.model_dump())
    return success_response(offer, "Offer sent successfully")


@router.post("/{offer_id}/counter", summary="Submit a counter-offer")
async def counter_offer(
    offer_id: str,
    data: CounterOfferRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    offer = await offer_service.counter_offer(db, current_user["id"], offer_id, data.counter_price, data.message)
    return success_response(offer, "Counter-offer submitted")


@router.post("/{offer_id}/respond", summary="Accept or Reject an offer (Accepting creates a Deal)")
async def respond_to_offer(
    offer_id: str,
    data: RespondOfferRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    res = await offer_service.respond_to_offer(db, current_user["id"], offer_id, data.accept)
    msg = "Offer accepted! Deal initialized." if data.accept else "Offer rejected."
    return success_response(res, msg)
