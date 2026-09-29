"""
Buyer Service — Registration, Profile Management, and Buyer Dashboard Analytics.
"""
import logging
from datetime import datetime, timezone, date
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.sql_models import UserModel, BuyerProfileModel, BuyerRequirementModel, OfferModel, DealModel, TransactionModel
from app.authentication.jwt_handler import hash_password, create_access_token, create_refresh_token
from app.utils.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.utils.helpers import serialize_doc

logger = logging.getLogger(__name__)


async def register_buyer(db: AsyncSession, user_data: dict, profile_data: dict) -> Dict:
    """Register a new buyer account + create buyer profile."""
    email = user_data["email"].lower()
    mobile = user_data["mobile_number"]

    # Check duplicate email
    res_e = await db.execute(select(UserModel).where(UserModel.email == email))
    if res_e.scalar_one_or_none():
        raise ConflictException("An account with this email already exists.")

    # Check duplicate phone
    res_m = await db.execute(select(UserModel).where(UserModel.mobile_number == mobile))
    if res_m.scalar_one_or_none():
        raise ConflictException("An account with this mobile number already exists.")

    now = datetime.now(timezone.utc)
    user = UserModel(
        full_name=user_data["full_name"],
        mobile_number=mobile,
        whatsapp_number=mobile,
        email=email,
        password=hash_password(user_data["password"]),
        village=user_data.get("village"),
        district=profile_data["district"],
        state=profile_data["state"],
        role="Buyer",
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    buyer_prof = BuyerProfileModel(
        user_id=user.id,
        company_name=profile_data["company_name"],
        owner_name=profile_data["owner_name"],
        gst_number=profile_data.get("gst_number"),
        business_license=profile_data.get("business_license"),
        address=profile_data.get("address"),
        district=profile_data["district"],
        state=profile_data["state"],
        pincode=profile_data.get("pincode"),
        latitude=profile_data.get("latitude"),
        longitude=profile_data.get("longitude"),
        buying_crops=profile_data.get("buying_crops", "Wheat, Onion, Tomato"),
        daily_capacity=float(profile_data.get("daily_capacity", 100.0)),
        preferred_payment_time=profile_data.get("preferred_payment_time", "Immediate"),
        bank_details=profile_data.get("bank_details"),
        verification_status="Verified",  # Auto-verified for seamless testing
        created_at=now,
        updated_at=now,
    )
    db.add(buyer_prof)
    await db.commit()
    await db.refresh(buyer_prof)

    access_token = create_access_token(user.id, "Buyer")
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": serialize_doc(user),
        "profile": serialize_doc(buyer_prof),
    }


async def list_buyers(db: AsyncSession) -> List[Dict]:
    """Get all registered real buyers with their buyer profiles."""
    stmt = (
        select(BuyerProfileModel, UserModel)
        .join(UserModel, BuyerProfileModel.user_id == UserModel.id)
        .order_by(BuyerProfileModel.created_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    out = []
    for prof, user in rows:
        p_dict = serialize_doc(prof)
        p_dict["user_id"] = user.id
        p_dict["full_name"] = user.full_name
        p_dict["mobile_number"] = user.mobile_number
        p_dict["whatsapp_number"] = user.mobile_number or user.whatsapp_number
        p_dict["email"] = user.email
        out.append(p_dict)
    return out


async def get_buyer_dashboard(db: AsyncSession, buyer_id: str) -> Dict:
    """Get consolidated buyer dashboard KPIs."""
    today = date.today()

    # Buying Requirements
    req_res = await db.execute(select(func.count(BuyerRequirementModel.id)).where(BuyerRequirementModel.buyer_id == buyer_id))
    total_reqs = req_res.scalar_one() or 0

    # Active Deals
    deal_res = await db.execute(select(func.count(DealModel.id)).where(
        and_(DealModel.buyer_id == buyer_id, DealModel.status != "Closed")
    ))
    active_deals = deal_res.scalar_one() or 0

    # Completed Purchases & Total Quantity
    tx_res = await db.execute(
        select(
            func.count(TransactionModel.id),
            func.coalesce(func.sum(TransactionModel.total_amount), 0.0),
            func.coalesce(func.sum(TransactionModel.quantity), 0.0),
            func.coalesce(func.avg(TransactionModel.final_price), 0.0)
        ).where(TransactionModel.buyer_id == buyer_id)
    )
    completed_txs, total_spent, total_qty, avg_price = tx_res.fetchone()

    # Pending Offers
    off_res = await db.execute(select(func.count(OfferModel.id)).where(
        and_(OfferModel.buyer_id == buyer_id, OfferModel.status == "Pending")
    ))
    pending_offers = off_res.scalar_one() or 0

    return {
        "todays_buying_requests": total_reqs,
        "active_deals": active_deals,
        "completed_purchases": completed_txs or 0,
        "pending_offers": pending_offers,
        "average_purchase_price": round(float(avg_price or 0.0), 2),
        "total_quantity_purchased": round(float(total_qty or 0.0), 1),
        "total_spent_amount": round(float(total_spent or 0.0), 2),
    }
