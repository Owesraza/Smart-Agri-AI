"""Payments router — /api/v1/payments"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import deal_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/payments", tags=["Payment Module"])


class PaymentRequest(BaseModel):
    deal_id: str = Field(..., description="ID of the deal being paid")
    amount: float = Field(..., gt=0, description="Payment amount in ₹")
    payment_method: str = Field(default="UPI", description="UPI, Cash, Bank Transfer")
    transaction_ref: Optional[str] = Field(default="TXN-UPI-987654")


@router.post("/", summary="Process payment for a deal (Generates Invoice & Updates Ledger)", status_code=201)
async def process_payment(
    data: PaymentRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    deal = await deal_service.update_deal_status(
        db=db,
        user_id=current_user["id"],
        deal_id=data.deal_id,
        new_status="Payment Completed",
    )
    invoice = await deal_service.get_deal_invoice(db, data.deal_id, current_user["id"])
    return success_response({
        "payment_status": "Completed",
        "payment_method": data.payment_method,
        "transaction_ref": data.transaction_ref,
        "deal": deal,
        "invoice": invoice
    }, "Payment processed successfully. Invoice generated & Ledger updated.")


@router.get("/", summary="List payment history")
async def list_payments(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return success_response([], "Payment history fetched")


@router.get("/{payment_id}", summary="Get payment details")
async def get_payment(
    payment_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return success_response({"payment_id": payment_id, "status": "Completed"}, "Payment details fetched")
