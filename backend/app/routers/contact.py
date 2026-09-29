"""Contact router — /api/v1/contact"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import marketplace_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/contact", tags=["WhatsApp Direct Contact"])


@router.get("/whatsapp-url", summary="Generate direct WhatsApp Click-to-Chat URL with target_user_id query param")
@router.get("/whatsapp/{user_id}", summary="Generate direct WhatsApp Click-to-Chat URL for a real registered user")
async def get_whatsapp_contact_endpoint(
    user_id: Optional[str] = None,
    target_user_id: Optional[str] = Query(default=None),
    crop: Optional[str] = Query(default="Wheat"),
    quantity: Optional[float] = Query(default=100.0),
    price: Optional[float] = Query(default=2300.0),
    contact_type: Optional[str] = Query(default="farmer_to_buyer"),  # buyer_to_farmer or farmer_to_buyer
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    target_id = target_user_id or user_id
    result = await marketplace_service.get_whatsapp_contact_url(
        db=db,
        target_user_id=target_id,
        sender_user_id=current_user["id"],
        crop=crop,
        quantity=quantity,
        price=price,
        contact_type=contact_type
    )
    return success_response(result, "WhatsApp Click-to-Chat URL generated")
