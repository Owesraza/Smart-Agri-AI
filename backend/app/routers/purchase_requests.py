"""Purchase Requests Router — /api/v1/requests & WhatsApp Click-to-Chat"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import purchase_request_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/requests", tags=["WhatsApp Communication & Purchase Requests"])


class PurchaseRequestCreate(BaseModel):
    crop_listing_id: str = Field(..., description="ID of target farmer crop listing")
    quantity: float = Field(..., gt=0, example=100.0)
    offered_price: float = Field(..., gt=0, example=2300.0)
    message: Optional[str] = Field(default=None, example="We are interested in buying your Wheat crop immediately.")


@router.post("/", summary="Create buyer purchase request (Triggers Farmer Notification)", status_code=201)
async def create_request_endpoint(
    data: PurchaseRequestCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    req = await purchase_request_service.create_purchase_request(
        db=db,
        buyer_id=current_user["id"],
        crop_listing_id=data.crop_listing_id,
        quantity=data.quantity,
        offered_price=data.offered_price,
        message=data.message,
    )
    return success_response(req, "Purchase request submitted to farmer.")


@router.get("/farmer", summary="Get purchase requests received by farmer")
async def get_farmer_requests_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    reqs = await purchase_request_service.get_farmer_purchase_requests(db, current_user["id"])
    return success_response(reqs, f"{len(reqs)} buyer purchase requests fetched")


@router.get("/buyer", summary="Get purchase requests sent by buyer")
async def get_buyer_requests_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    reqs = await purchase_request_service.get_buyer_purchase_requests(db, current_user["id"])
    return success_response(reqs, f"{len(reqs)} submitted purchase requests fetched")


@router.put("/{id}/accept", summary="Accept purchase request (Creates Deal & WhatsApp Link)")
async def accept_request_endpoint(
    id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    res = await purchase_request_service.accept_purchase_request(db, current_user["id"], id)
    return success_response(res, "Request accepted! Deal created & WhatsApp link generated.")


@router.put("/{id}/reject", summary="Reject purchase request")
async def reject_request_endpoint(
    id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    res = await purchase_request_service.reject_purchase_request(db, current_user["id"], id)
    return success_response(res, "Purchase request rejected.")


@router.get("/{id}/whatsapp", summary="Generate WhatsApp Click-to-Chat URL for a request")
async def get_whatsapp_url_endpoint(
    id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    reqs = await purchase_request_service.get_farmer_purchase_requests(db, current_user["id"])
    target = next((r for r in reqs if r["id"] == id), None)
    if not target:
        reqs = await purchase_request_service.get_buyer_purchase_requests(db, current_user["id"])
        target = next((r for r in reqs if r["id"] == id), None)

    if not target:
        return success_response({"whatsapp_url": "https://wa.me/919876543210"}, "Default WhatsApp link")

    return success_response({"whatsapp_url": target["whatsapp_url"]}, "WhatsApp chat link generated")
