"""Deals router — /api/v1/deals"""
import urllib.parse
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import deal_service
from app.services.purchase_request_service import format_whatsapp_phone
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/deals", tags=["Deal Workflow & Invoices"])


class DealStatusUpdateRequest(BaseModel):
    new_status: str = Field(..., example="Harvest Scheduled", description="Offer Accepted, Harvest Scheduled, Packaging, Transport, Delivered, Payment Completed, Closed")
    transport_cost: Optional[float] = Field(default=0.0)
    packaging_cost: Optional[float] = Field(default=0.0)


@router.get("/my", summary="Get all user deal contracts & workflow timelines")
async def list_user_deals_endpoint(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    deals = await deal_service.get_user_deals(db, current_user["id"])
    return success_response(deals, f"{len(deals)} deal contracts fetched")


@router.get("/{deal_id}", summary="Get deal details & workflow timeline")
async def get_deal_endpoint(
    deal_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    deal = await deal_service.get_deal(db, deal_id, current_user["id"])
    return success_response(deal, "Deal details fetched")


@router.get("/{deal_id}/invoice", summary="Get deal transaction invoice details")
async def get_deal_invoice_endpoint(
    deal_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    inv = await deal_service.get_deal_invoice(db, deal_id, current_user["id"])
    return success_response(inv, "Deal invoice details fetched")


@router.get("/{deal_id}/whatsapp", summary="Generate WhatsApp chat link for a deal")
async def get_deal_whatsapp_endpoint(
    deal_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    inv = await deal_service.get_deal_invoice(db, deal_id, current_user["id"])
    phone = inv.get("farmer_mobile") if current_user["id"] != inv.get("farmer_id") else inv.get("buyer_mobile", "919876543210")
    clean_phone = format_whatsapp_phone(phone or "919876543210")

    msg_text = (
        f"Hello,\n"
        f"Your SmartAgri AI crop deal request has been accepted.\n\n"
        f"Crop: {inv.get('crop', 'Wheat')}\n"
        f"Quantity: {inv.get('quantity', 50)} Quintals\n"
        f"Agreed Price: ₹{inv.get('final_price', 2300)}/Qtl\n\n"
        f"Please continue discussion regarding delivery and payment.\n\n"
        f"Thank You."
    )
    encoded = urllib.parse.quote(msg_text)
    url = f"https://wa.me/{clean_phone}?text={encoded}"
    return success_response({"whatsapp_url": url}, "WhatsApp chat link generated")


@router.patch("/{deal_id}/status", summary="Advance deal workflow step (Payment Completed auto-syncs Ledger)")
@router.put("/{deal_id}/status", summary="Advance deal workflow step alias")
async def update_deal_status_endpoint(
    deal_id: str,
    data: DealStatusUpdateRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    deal = await deal_service.update_deal_status(
        db=db,
        user_id=current_user["id"],
        deal_id=deal_id,
        new_status=data.new_status,
        transport_cost=data.transport_cost,
        packaging_cost=data.packaging_cost,
    )
    return success_response(deal, f"Deal workflow updated to '{data.new_status}'")


class OrderStatusUpdateRequest(BaseModel):
    order_status: str = Field(..., description="Dispatched, Out for Delivery, Delivered")
    transport_cost: Optional[float] = Field(default=0.0)
    packaging_cost: Optional[float] = Field(default=0.0)


@router.patch("/{deal_id}/order-status", summary="Advance Order Tracking Delivery Status")
@router.put("/{deal_id}/order-status", summary="Advance Order Tracking Delivery Status alias")
async def update_order_status_endpoint(
    deal_id: str,
    data: OrderStatusUpdateRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    deal = await deal_service.update_order_delivery_status(
        db=db,
        user_id=current_user["id"],
        deal_id=deal_id,
        new_order_status=data.order_status,
        transport_cost=data.transport_cost,
        packaging_cost=data.packaging_cost,
    )
    return success_response(deal, f"Order status updated to '{data.order_status}'")

