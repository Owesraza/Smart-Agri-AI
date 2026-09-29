"""
Purchase Request Service — WhatsApp Click-to-Chat & Deal Creation Engine.
Manages buyer crop purchase requests, farmer acceptances, WhatsApp link generation, and deal pipeline synchronization.
"""
import logging
import json
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.sql_models import (
    PurchaseRequestModel, CropListingModel, UserModel, DealModel, OfferModel, NotificationModel,
    RatingModel
)
from app.services.notification_service import create_notification
from app.utils.distance_calculator import calculate_delivery_estimate
from app.utils.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.utils.helpers import serialize_doc, serialize_list

logger = logging.getLogger(__name__)


def format_whatsapp_phone(phone: str) -> str:
    """Format phone number for WhatsApp wa.me link (e.g. 919876543210)."""
    digits = ''.join(filter(str.isdigit, phone or ''))
    if len(digits) == 10:
        return f"91{digits}"
    return digits if digits else "919876543210"


def generate_whatsapp_chat_url(phone: str, crop: str, quantity: float, price: float, role_name: str = "Buyer") -> str:
    """Generate dynamic WhatsApp Click-to-Chat URL."""
    clean_phone = format_whatsapp_phone(phone)
    msg_text = (
        f"Hello,\n"
        f"Your SmartAgri AI crop deal request has been accepted.\n\n"
        f"Crop: {crop}\n"
        f"Quantity: {quantity} Quintals\n"
        f"Agreed Price: ₹{price}/Qtl\n\n"
        f"Let's finalize logistics and delivery schedule.\n"
        f"— Smart Agri AI CropPoint"
    )
    encoded_text = urllib.parse.quote(msg_text)
    return f"https://wa.me/{clean_phone}?text={encoded_text}"


async def create_purchase_request(
    db: AsyncSession,
    crop_listing_id: str,
    buyer_id: str,
    offered_price: float,
    quantity: float,
    message: Optional[str] = None
) -> Dict:
    """Create a buyer purchase request for a farmer's crop listing."""
    # Fetch listing
    res = await db.execute(select(CropListingModel).where(CropListingModel.id == crop_listing_id))
    listing = res.scalar_one_or_none()
    if not listing:
        raise NotFoundException("Crop listing")

    if listing.farmer_id == buyer_id:
        raise ForbiddenException("You cannot submit a purchase request on your own crop listing.")

    if listing.status != "ACTIVE":
        raise BadRequestException(f"Cannot request listing with status '{listing.status}'")

    if quantity > listing.quantity:
        raise BadRequestException(f"Requested quantity ({quantity}) exceeds available quantity ({listing.quantity})")

    # Fetch buyer
    res_b = await db.execute(select(UserModel).where(UserModel.id == buyer_id))
    buyer = res_b.scalar_one_or_none()
    buyer_name = buyer.full_name if buyer else "A verified buyer"

    # Create request
    now = datetime.now(timezone.utc)
    req = PurchaseRequestModel(
        crop_listing_id=crop_listing_id,
        buyer_id=buyer_id,
        farmer_id=listing.farmer_id,
        offered_price=offered_price,
        quantity=quantity,
        message=message,
        status="Pending",
        created_at=now,
        updated_at=now,
    )
    db.add(req)

    # Create Notification for Farmer
    await create_notification(
        db=db,
        user_id=listing.farmer_id,
        title="🌾 New Purchase Request Received!",
        message=f"{buyer_name} submitted a purchase request for {quantity} Qtl of your {listing.crop} at ₹{offered_price}/Qtl.",
        type_="Request"
    )

    await db.commit()
    await db.refresh(req)
    return serialize_doc(req)


async def get_farmer_purchase_requests(db: AsyncSession, farmer_id: str) -> List[Dict]:
    """Get all purchase requests received by a farmer for their listings."""
    stmt = (
        select(PurchaseRequestModel, UserModel, CropListingModel)
        .join(UserModel, PurchaseRequestModel.buyer_id == UserModel.id)
        .join(CropListingModel, PurchaseRequestModel.crop_listing_id == CropListingModel.id)
        .where(PurchaseRequestModel.farmer_id == farmer_id)
        .order_by(PurchaseRequestModel.created_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    out = []
    for req, buyer, listing in rows:
        r_dict = serialize_doc(req)
        r_dict["buyer_name"] = buyer.full_name
        r_dict["buyer_mobile"] = buyer.mobile_number
        r_dict["buyer_whatsapp"] = buyer.mobile_number or buyer.whatsapp_number
        r_dict["buyer_district"] = buyer.district
        r_dict["crop"] = listing.crop
        r_dict["listing_location"] = listing.location
        r_dict["agreed_price"] = req.offered_price
        r_dict["total_amount"] = round(req.quantity * req.offered_price, 2)
        r_dict["whatsapp_url"] = generate_whatsapp_chat_url(
            phone=buyer.mobile_number or buyer.whatsapp_number,
            crop=listing.crop,
            quantity=req.quantity,
            price=req.offered_price,
            role_name="Buyer"
        )
        if req.status and req.status.lower() == "accepted":
            res_d = await db.execute(select(DealModel).where(DealModel.request_id == req.id))
            deal = res_d.scalar_one_or_none()
            if deal:
                r_dict["deal_id"] = deal.id
                r_dict["order_number"] = deal.order_number or f"ORD-{req.id[:8].upper()}"
                r_dict["order_status"] = deal.order_status or "Order Confirmed"
                r_dict["distance_km"] = deal.distance_km
                r_dict["expected_delivery_date"] = deal.expected_delivery_date.isoformat() if deal.expected_delivery_date else None
                r_dict["formatted_expected_date"] = deal.expected_delivery_date.strftime("%d %b %Y") if deal.expected_delivery_date else None
                r_dict["dispatched_at"] = deal.dispatched_at.isoformat() if deal.dispatched_at else None
                r_dict["out_for_delivery_at"] = deal.out_for_delivery_at.isoformat() if deal.out_for_delivery_at else None
                r_dict["delivered_at"] = deal.delivered_at.isoformat() if deal.delivered_at else None
                r_dict["source_location"] = deal.source_location or listing.location or "Pune"
                r_dict["destination_location"] = deal.destination_location or buyer.district or "Nashik"

                # Check rating from farmer to buyer
                res_rate = await db.execute(
                    select(RatingModel).where(
                        RatingModel.deal_id == deal.id,
                        RatingModel.from_user_id == farmer_id
                    )
                )
                user_rate = res_rate.scalar_one_or_none()
                r_dict["has_rated"] = (user_rate is not None)
                r_dict["user_rating"] = user_rate.rating if user_rate else None
                r_dict["can_rate"] = (deal.order_status == "Delivered" and user_rate is None)
        out.append(r_dict)
    return out


async def get_buyer_purchase_requests(db: AsyncSession, buyer_id: str) -> List[Dict]:
    """Get all purchase requests sent by a buyer."""
    stmt = (
        select(PurchaseRequestModel, UserModel, CropListingModel)
        .join(UserModel, PurchaseRequestModel.farmer_id == UserModel.id)
        .join(CropListingModel, PurchaseRequestModel.crop_listing_id == CropListingModel.id)
        .where(PurchaseRequestModel.buyer_id == buyer_id)
        .order_by(PurchaseRequestModel.created_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    out = []
    for req, farmer, listing in rows:
        r_dict = serialize_doc(req)
        r_dict["farmer_name"] = farmer.full_name
        r_dict["farmer_mobile"] = farmer.mobile_number
        r_dict["farmer_whatsapp"] = farmer.mobile_number or farmer.whatsapp_number
        r_dict["farmer_district"] = farmer.district
        r_dict["crop"] = listing.crop
        r_dict["listing_location"] = listing.location
        r_dict["agreed_price"] = req.offered_price
        r_dict["total_amount"] = round(req.quantity * req.offered_price, 2)
        r_dict["whatsapp_url"] = generate_whatsapp_chat_url(
            phone=farmer.mobile_number or farmer.whatsapp_number,
            crop=listing.crop,
            quantity=req.quantity,
            price=req.offered_price,
            role_name="Farmer"
        )
        if req.status and req.status.lower() == "accepted":
            res_d = await db.execute(select(DealModel).where(DealModel.request_id == req.id))
            deal = res_d.scalar_one_or_none()
            if deal:
                r_dict["deal_id"] = deal.id
                r_dict["order_number"] = deal.order_number or f"ORD-{req.id[:8].upper()}"
                r_dict["order_status"] = deal.order_status or "Order Confirmed"
                r_dict["distance_km"] = deal.distance_km
                r_dict["expected_delivery_date"] = deal.expected_delivery_date.isoformat() if deal.expected_delivery_date else None
                r_dict["formatted_expected_date"] = deal.expected_delivery_date.strftime("%d %b %Y") if deal.expected_delivery_date else None
                r_dict["dispatched_at"] = deal.dispatched_at.isoformat() if deal.dispatched_at else None
                r_dict["out_for_delivery_at"] = deal.out_for_delivery_at.isoformat() if deal.out_for_delivery_at else None
                r_dict["delivered_at"] = deal.delivered_at.isoformat() if deal.delivered_at else None
                r_dict["source_location"] = deal.source_location or listing.location or "Pune"
                r_dict["destination_location"] = deal.destination_location or farmer.district or "Nashik"

                # Check rating from buyer to farmer
                res_rate = await db.execute(
                    select(RatingModel).where(
                        RatingModel.deal_id == deal.id,
                        RatingModel.from_user_id == buyer_id
                    )
                )
                user_rate = res_rate.scalar_one_or_none()
                r_dict["has_rated"] = (user_rate is not None)
                r_dict["user_rating"] = user_rate.rating if user_rate else None
                r_dict["can_rate"] = (deal.order_status == "Delivered" and user_rate is None)
        out.append(r_dict)
    return out


async def accept_purchase_request(db: AsyncSession, farmer_id: str, request_id: str) -> Dict:
    """Accept purchase request, create deal contract, and format WhatsApp communication link."""
    res = await db.execute(select(PurchaseRequestModel).where(PurchaseRequestModel.id == request_id))
    req = res.scalar_one_or_none()
    if not req:
        raise NotFoundException("Purchase request")

    if req.farmer_id != farmer_id:
        raise ForbiddenException("You can only accept requests for your own crop listings.")

    if req.status == "Accepted":
        raise BadRequestException("This purchase request has already been accepted.")
    if req.status == "Rejected":
        raise BadRequestException("Cannot accept a purchase request that has already been rejected.")

    now = datetime.now(timezone.utc)
    req.status = "Accepted"
    req.updated_at = now

    # Fetch crop listing
    res_l = await db.execute(select(CropListingModel).where(CropListingModel.id == req.crop_listing_id))
    listing = res_l.scalar_one_or_none()
    crop_name = listing.crop if listing else "Wheat"

    # Fetch Buyer and Farmer details
    res_b = await db.execute(select(UserModel).where(UserModel.id == req.buyer_id))
    buyer = res_b.scalar_one_or_none()

    res_f = await db.execute(select(UserModel).where(UserModel.id == farmer_id))
    farmer = res_f.scalar_one_or_none()

    # Ensure a matching OfferModel exists to satisfy legacy deals.offer_id NOT NULL constraint
    res_offer = await db.execute(select(OfferModel).where(OfferModel.id == req.id))
    offer = res_offer.scalar_one_or_none()
    if not offer:
        offer = OfferModel(
            id=req.id,
            listing_id=req.crop_listing_id,
            buyer_id=req.buyer_id,
            farmer_id=farmer_id,
            offered_price=req.offered_price,
            message=req.message,
            status="Accepted",
            created_at=now,
            updated_at=now,
        )
        db.add(offer)

    # Calculate dynamic delivery estimate and generate Order Number
    source_location = farmer.district or (listing.location if listing else None) or "Pune"
    dest_location = buyer.district or "Nashik" if buyer else "Nashik"
    delivery_calc = calculate_delivery_estimate(source_location, dest_location)
    order_number = f"ORD-{req.id[:8].upper()}"

    # Create Deal entry automatically with Order Confirmed status
    initial_timeline = [
        {"step": "Order Confirmed", "status": "Completed", "timestamp": now.isoformat()},
        {"step": "Dispatched", "status": "Pending", "timestamp": None},
        {"step": "Out for Delivery", "status": "Pending", "timestamp": None},
        {"step": "Delivered", "status": "Pending", "timestamp": None},
        {"step": "WhatsApp Communication Started", "status": "In Progress", "timestamp": now.isoformat()},
        {"step": "Negotiation", "status": "Completed", "timestamp": now.isoformat()},
        {"step": "Deal Confirmed", "status": "Completed", "timestamp": now.isoformat()},
        {"step": "Harvest", "status": "Pending", "timestamp": None},
        {"step": "Delivery", "status": "Pending", "timestamp": None},
        {"step": "Payment Completed", "status": "Pending", "timestamp": None},
        {"step": "Ledger Updated", "status": "Pending", "timestamp": None},
    ]

    deal = DealModel(
        offer_id=offer.id,
        request_id=req.id,
        listing_id=req.crop_listing_id,
        buyer_id=req.buyer_id,
        farmer_id=farmer_id,
        status="Farmer Accepted",
        order_status="Order Confirmed",
        order_number=order_number,
        source_location=source_location,
        destination_location=dest_location,
        distance_km=delivery_calc["distance_km"],
        expected_delivery_date=delivery_calc["expected_delivery_date"],
        timeline_json=json.dumps(initial_timeline),
        created_at=now,
        updated_at=now,
    )
    db.add(deal)

    # Send Order Confirmed Notifications to both Buyer and Farmer
    await create_notification(
        db=db,
        user_id=req.buyer_id,
        title="✅ Order Confirmed!",
        message=f"Your order #{order_number} for {crop_name} ({req.quantity} Qtl) has been confirmed by {farmer.full_name if farmer else 'Farmer'}. Expected Delivery: {delivery_calc['formatted_expected_date']}.",
        type_="Deal"
    )
    await create_notification(
        db=db,
        user_id=farmer_id,
        title="📦 Order Confirmed",
        message=f"Order #{order_number} confirmed for buyer {buyer.full_name if buyer else 'Buyer'}. Expected delivery: {delivery_calc['formatted_expected_date']} ({delivery_calc['distance_km']} km).",
        type_="Deal"
    )

    await db.commit()
    await db.refresh(req)

    whatsapp_url = generate_whatsapp_chat_url(
        phone=buyer.mobile_number or buyer.whatsapp_number if buyer else "919876543210",
        crop=crop_name,
        quantity=req.quantity,
        price=req.offered_price,
        role_name="Buyer"
    )

    r_dict = serialize_doc(req)
    r_dict["deal_id"] = deal.id
    r_dict["order_number"] = order_number
    r_dict["order_status"] = "Order Confirmed"
    r_dict["distance_km"] = delivery_calc["distance_km"]
    r_dict["expected_delivery_date"] = delivery_calc["expected_delivery_date"].isoformat()
    r_dict["formatted_expected_date"] = delivery_calc["formatted_expected_date"]
    r_dict["source_location"] = source_location
    r_dict["destination_location"] = dest_location
    r_dict["buyer_name"] = buyer.full_name if buyer else "Buyer"
    r_dict["buyer_mobile"] = buyer.mobile_number if buyer else ""
    r_dict["buyer_whatsapp"] = buyer.mobile_number or buyer.whatsapp_number if buyer else ""
    r_dict["whatsapp_url"] = whatsapp_url
    return r_dict


async def reject_purchase_request(db: AsyncSession, farmer_id: str, request_id: str) -> Dict:
    """Reject purchase request."""
    res = await db.execute(select(PurchaseRequestModel).where(PurchaseRequestModel.id == request_id))
    req = res.scalar_one_or_none()
    if not req:
        raise NotFoundException("Purchase request")

    if req.farmer_id != farmer_id:
        raise ForbiddenException("You can only reject requests for your own crop listings.")

    if req.status in ["Accepted", "Rejected"]:
        raise BadRequestException(f"Cannot reject purchase request that is already {req.status.lower()}.")

    now = datetime.now(timezone.utc)
    req.status = "Rejected"
    req.updated_at = now

    await create_notification(
        db=db,
        user_id=req.buyer_id,
        title="❌ Request Update",
        message="Your purchase request was declined by the farmer.",
        type_="Request"
    )

    await db.commit()
    await db.refresh(req)
    return serialize_doc(req)
