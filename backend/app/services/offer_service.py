"""
Offer Service — Offer Creation, Counter-Offers, Acceptance & Rejection.
When an offer is accepted:
- Automatically creates a `DealModel` (Offer Accepted -> Harvest Scheduled -> Packaging -> Transport -> Delivered -> Payment Completed -> Closed)
- Automatically initializes a `ConversationModel` for real-time WebSocket chat
- Sends real-time notifications to both Farmer & Buyer
"""
import logging
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.sql_models import OfferModel, CropListingModel, BuyerRequirementModel, DealModel, ConversationModel
from app.services.notification_service import create_notification
from app.utils.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.utils.helpers import serialize_doc, serialize_list

logger = logging.getLogger(__name__)


async def create_offer(db: AsyncSession, buyer_id: str, data: dict) -> Dict:
    """Create a new buying offer on a farmer crop listing or requirement."""
    listing_id = data.get("listing_id")
    farmer_id = data.get("farmer_id")

    if listing_id and not farmer_id:
        res_l = await db.execute(select(CropListingModel).where(CropListingModel.id == listing_id))
        listing = res_l.scalar_one_or_none()
        if not listing:
            raise NotFoundException("Crop listing")
        farmer_id = listing.farmer_id

    if not farmer_id:
        raise BadRequestException("Farmer ID is required for sending an offer.")

    now = datetime.now(timezone.utc)
    offer = OfferModel(
        listing_id=listing_id,
        requirement_id=data.get("requirement_id"),
        buyer_id=buyer_id,
        farmer_id=farmer_id,
        offered_price=float(data["offered_price"]),
        message=data.get("message"),
        expected_pickup_date=data.get("expected_pickup_date"),
        status="Pending",
        created_at=now,
        updated_at=now,
    )
    db.add(offer)
    await db.commit()
    await db.refresh(offer)

    # Notify Farmer
    await create_notification(
        db=db,
        user_id=farmer_id,
        title="💼 New Offer Received!",
        message=f"A buyer sent an offer of ₹{offer.offered_price}/quintal.",
        type_="Offer"
    )

    return serialize_doc(offer)


async def counter_offer(db: AsyncSession, user_id: str, offer_id: str, counter_price: float, message: str = None) -> Dict:
    """Submit a counter-offer."""
    res_o = await db.execute(select(OfferModel).where(OfferModel.id == offer_id))
    offer = res_o.scalar_one_or_none()
    if not offer:
        raise NotFoundException("Offer")

    if user_id not in (offer.farmer_id, offer.buyer_id):
        raise ForbiddenException("You cannot counter this offer.")

    offer.counter_price = float(counter_price)
    offer.status = "Counter Offer"
    offer.message = message or offer.message
    offer.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(offer)

    recipient = offer.buyer_id if user_id == offer.farmer_id else offer.farmer_id
    await create_notification(
        db=db,
        user_id=recipient,
        title="🔄 Counter-Offer Received!",
        message=f"Counter-offer of ₹{counter_price}/quintal proposed.",
        type_="Offer"
    )

    return serialize_doc(offer)


async def respond_to_offer(db: AsyncSession, user_id: str, offer_id: str, accept: bool) -> Dict:
    """Accept or Reject an offer. If accepted, creates Deal and Conversation."""
    res_o = await db.execute(select(OfferModel).where(OfferModel.id == offer_id))
    offer = res_o.scalar_one_or_none()
    if not offer:
        raise NotFoundException("Offer")

    if user_id not in (offer.farmer_id, offer.buyer_id):
        raise ForbiddenException("You do not have access to this offer.")

    now = datetime.now(timezone.utc)

    if not accept:
        offer.status = "Rejected"
        offer.updated_at = now
        await db.commit()
        return {"offer": serialize_doc(offer), "status": "Rejected"}

    # Accept Offer -> Create Deal & Conversation
    offer.status = "Accepted"
    offer.updated_at = now

    initial_timeline = [
        {"step": "Offer Accepted", "status": "Completed", "timestamp": now.isoformat()},
        {"step": "Harvest Scheduled", "status": "Pending", "timestamp": None},
        {"step": "Packaging", "status": "Pending", "timestamp": None},
        {"step": "Transport & Pickup", "status": "Pending", "timestamp": None},
        {"step": "Delivered & Payment", "status": "Pending", "timestamp": None},
    ]

    deal = DealModel(
        offer_id=offer.id,
        listing_id=offer.listing_id,
        requirement_id=offer.requirement_id,
        buyer_id=offer.buyer_id,
        farmer_id=offer.farmer_id,
        status="Offer Accepted",
        timeline_json=json.dumps(initial_timeline),
        created_at=now,
        updated_at=now,
    )
    db.add(deal)

    # Initialize Conversation for real-time chat
    conv = ConversationModel(
        user1_id=offer.buyer_id,
        user2_id=offer.farmer_id,
        listing_id=offer.listing_id,
        offer_id=offer.id,
        last_message="Offer accepted! Conversation started.",
        updated_at=now,
    )
    db.add(conv)

    await db.commit()
    await db.refresh(deal)
    await db.refresh(conv)

    # Notify both
    await create_notification(db=db, user_id=offer.buyer_id, title="🎉 Offer Accepted!", message="The farmer accepted your offer. Deal initialized!", type_="Deal")
    await create_notification(db=db, user_id=offer.farmer_id, title="🤝 Deal Initialized!", message="Offer accepted. Follow the deal workflow.", type_="Deal")

    return {
        "offer": serialize_doc(offer),
        "deal": serialize_doc(deal),
        "conversation_id": conv.id,
    }
