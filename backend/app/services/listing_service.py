"""
Listing Service — Complete CRUD for Crop Listings.
Secured with JWT authentication and strict farmer ownership validation.
"""
import logging
from datetime import datetime, timezone, date
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_

from app.models.sql_models import CropListingModel, BuyerProfileModel, UserModel, PurchaseRequestModel
from app.services.market_service import normalize_crop_name, calculate_advance_booking_discount
from app.services.notification_service import create_notification
from app.utils.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.utils.helpers import serialize_doc, serialize_list, paginate, pagination_meta

logger = logging.getLogger(__name__)


def _enrich_listing_with_dynamic_advance_discount(doc: dict) -> dict:
    """
    Dynamically recalculate the remaining advance booking days and discount tier
    based on elapsed calendar days since the listing was created.
    Example: 10 days initial -> after 5 days -> 5 days remaining (tier updates to 5% OFF).
    """
    initial_advance_days = int(doc.get("advance_days") or 0)
    created_at_str = doc.get("created_at")
    expected_price = float(doc.get("expected_price") or 0.0)
    quantity = float(doc.get("quantity") or 0.0)

    if initial_advance_days > 0 and created_at_str and expected_price > 0:
        try:
            if isinstance(created_at_str, str):
                created_dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                if created_dt.tzinfo is None:
                    created_dt = created_dt.replace(tzinfo=timezone.utc)
            elif isinstance(created_at_str, datetime):
                created_dt = created_at_str if created_at_str.tzinfo else created_at_str.replace(tzinfo=timezone.utc)
            else:
                created_dt = datetime.now(timezone.utc)

            now_dt = datetime.now(timezone.utc)
            elapsed_days = max(0, (now_dt.date() - created_dt.date()).days)
            remaining_days = max(0, initial_advance_days - elapsed_days)

            # Recalculate dynamic time-decay tier based on REMAINING days
            disc_info = calculate_advance_booking_discount(
                base_price=expected_price,
                quantity_quintals=quantity,
                days_in_advance=remaining_days
            )

            doc["initial_advance_days"] = initial_advance_days
            doc["remaining_advance_days"] = remaining_days
            doc["elapsed_days"] = elapsed_days
            doc["discount_pct"] = disc_info["discount_pct"]
            doc["discounted_price"] = disc_info["discounted_price_per_quintal"]
            doc["tier_label"] = disc_info["tier_label"]
            doc["tier_description"] = disc_info["description"]
        except Exception as e:
            logger.warning(f"Error computing dynamic advance discount: {e}")
            doc["initial_advance_days"] = initial_advance_days
            doc["remaining_advance_days"] = initial_advance_days
            doc["elapsed_days"] = 0
            doc["tier_label"] = "🌟 Advance Booking"
    else:
        doc["initial_advance_days"] = 0
        doc["remaining_advance_days"] = 0
        doc["elapsed_days"] = 0
        doc["discount_pct"] = 0.0
        doc["discounted_price"] = expected_price
        doc["tier_label"] = "🛒 Spot Market Rate"
        doc["tier_description"] = "Immediate delivery rate."

    return doc


async def create_crop_listing(db: AsyncSession, farmer_id: str, data: dict) -> Dict:
    """Create a new crop listing for an authenticated farmer."""
    crop_norm = normalize_crop_name(data["crop"])
    now = datetime.now(timezone.utc)
    
    exp_price = float(data["expected_price"])
    qty = float(data["quantity"])
    adv_days = int(data.get("advance_days") or 0)
    
    disc_pct = 0.0
    disc_price = exp_price
    if adv_days > 0:
        disc_info = calculate_advance_booking_discount(
            base_price=exp_price,
            quantity_quintals=qty,
            days_in_advance=adv_days
        )
        disc_pct = disc_info["discount_pct"]
        disc_price = disc_info["discounted_price_per_quintal"]

    listing = CropListingModel(
        farmer_id=farmer_id,
        plot_id=data.get("plot_id"),
        crop=crop_norm,
        quantity=qty,
        expected_price=exp_price,
        harvest_date=data.get("harvest_date"),
        quality_grade=data.get("quality_grade", "Grade A"),
        location=data.get("location", "Nashik APMC Yard"),
        available_until=data.get("available_until"),
        photo_url=data.get("photo_url"),
        advance_days=adv_days,
        discount_pct=disc_pct,
        discounted_price=disc_price,
        status=data.get("status", "ACTIVE").upper(),
        created_at=now,
        updated_at=now,
    )
    db.add(listing)
    await db.commit()
    await db.refresh(listing)

    # Notify matching buyers
    try:
        res_b = await db.execute(select(BuyerProfileModel).where(BuyerProfileModel.buying_crops.ilike(f"%{crop_norm}%")))
        buyers = res_b.scalars().all()
        for b in buyers:
            await create_notification(
                db=db,
                user_id=b.user_id,
                title=f"🌾 New {crop_norm} Listed!",
                message=f"Farmer in {listing.location} listed {listing.quantity} quintals of {crop_norm} @ ₹{listing.expected_price}/Qtl.",
                type_="Match"
            )
    except Exception as e:
        logger.warning(f"Failed to send buyer notifications: {e}")

    logger.info(f"✅ Crop Listing created ID: {listing.id} for farmer: {farmer_id}")
    return _enrich_listing_with_dynamic_advance_discount(serialize_doc(listing))


async def get_all_active_listings(
    db: AsyncSession,
    crop: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = 1,
    limit: int = 20,
) -> Dict:
    """Retrieve all ACTIVE crop listings for buyers and public marketplace with farmer details and dynamic time-decay discount."""
    p = paginate(page, limit)
    stmt = (
        select(
            CropListingModel,
            UserModel.full_name,
            UserModel.mobile_number,
            UserModel.village,
            UserModel.district
        )
        .join(UserModel, CropListingModel.farmer_id == UserModel.id, isouter=True)
        .where(
            or_(
                CropListingModel.status == "ACTIVE",
                CropListingModel.status == "Available",
                CropListingModel.status == "active"
            )
        )
    )
    
    if crop:
        stmt = stmt.where(CropListingModel.crop.ilike(f"%{crop}%"))
    if location:
        stmt = stmt.where(CropListingModel.location.ilike(f"%{location}%"))
    if min_price:
        stmt = stmt.where(CropListingModel.expected_price >= min_price)
    if max_price:
        stmt = stmt.where(CropListingModel.expected_price <= max_price)

    count_stmt = select(func.count(CropListingModel.id)).where(
        or_(
            CropListingModel.status == "ACTIVE",
            CropListingModel.status == "Available",
            CropListingModel.status == "active"
        )
    )
    total_res = await db.execute(count_stmt)
    total = total_res.scalar_one() or 0

    res = await db.execute(stmt.order_by(CropListingModel.created_at.desc()).offset(p["offset"]).limit(p["limit"]))
    rows = res.all()

    enriched = []
    for l_item, f_name, f_mobile, f_village, f_district in rows:
        doc = serialize_doc(l_item)
        doc["farmer_name"] = f_name or "Verified Farmer"
        doc["farmer_mobile"] = f_mobile or ""
        doc["farmer_village"] = f_village or ""
        doc["farmer_district"] = f_district or doc.get("location", "Maharashtra")
        enriched.append(_enrich_listing_with_dynamic_advance_discount(doc))

    return {"listings": enriched, "pagination": pagination_meta(total, page, p["limit"])}


async def ensure_baseline_farmer_listings(db: AsyncSession, farmer_id: str):
    """No-op: baseline dummy listings seeding disabled permanently."""
    return


async def get_farmer_own_listings(
    db: AsyncSession,
    farmer_id: str,
    page: int = 1,
    limit: int = 20,
) -> Dict:
    """Retrieve current authenticated farmer's own listings with dynamic time-decay discount."""
    p = paginate(page, limit)
    stmt = select(CropListingModel).where(CropListingModel.farmer_id == farmer_id)
    
    count_stmt = select(func.count(CropListingModel.id)).where(CropListingModel.farmer_id == farmer_id)
    total_res = await db.execute(count_stmt)
    total = total_res.scalar_one() or 0

    res = await db.execute(stmt.order_by(CropListingModel.created_at.desc()).offset(p["offset"]).limit(p["limit"]))
    listings = res.scalars().all()

    enriched = [_enrich_listing_with_dynamic_advance_discount(x) for x in serialize_list(listings)]
    return {"listings": enriched, "pagination": pagination_meta(total, page, p["limit"])}


async def get_listing_by_id(db: AsyncSession, listing_id: str) -> Dict:
    """Retrieve a single crop listing by ID with dynamic time-decay discount."""
    res = await db.execute(select(CropListingModel).where(CropListingModel.id == listing_id))
    listing = res.scalar_one_or_none()
    if not listing:
        raise NotFoundException("Crop listing")
    return _enrich_listing_with_dynamic_advance_discount(serialize_doc(listing))


async def update_crop_listing(db: AsyncSession, farmer_id: str, listing_id: str, data: dict) -> Dict:
    """Update a crop listing (Secured: Only owner farmer can update)."""
    res = await db.execute(select(CropListingModel).where(CropListingModel.id == listing_id))
    listing = res.scalar_one_or_none()
    if not listing:
        raise NotFoundException("Crop listing")

    if listing.farmer_id != farmer_id:
        raise ForbiddenException("You do not have permission to edit this listing.")

    now = datetime.now(timezone.utc)
    for field in ["crop", "quantity", "expected_price", "harvest_date", "quality_grade", "location", "available_until", "photo_url", "plot_id", "status", "advance_days"]:
        if field in data and data[field] is not None:
            if field == "crop":
                setattr(listing, field, normalize_crop_name(data[field]))
            elif field == "status":
                setattr(listing, field, str(data[field]).upper())
            else:
                setattr(listing, field, data[field])

    # Recompute advance discount on update if expected_price or advance_days changed
    if listing.advance_days and listing.advance_days > 0 and listing.expected_price:
        disc_info = calculate_advance_booking_discount(
            base_price=float(listing.expected_price),
            quantity_quintals=float(listing.quantity),
            days_in_advance=int(listing.advance_days)
        )
        listing.discount_pct = disc_info["discount_pct"]
        listing.discounted_price = disc_info["discounted_price_per_quintal"]

    listing.updated_at = now
    await db.commit()
    await db.refresh(listing)

    logger.info(f"✅ Crop Listing updated ID: {listing_id} by farmer: {farmer_id}")
    return _enrich_listing_with_dynamic_advance_discount(serialize_doc(listing))


async def delete_crop_listing(db: AsyncSession, farmer_id: str, listing_id: str) -> bool:
    """Delete a crop listing (Secured: Only owner farmer can delete)."""
    res = await db.execute(select(CropListingModel).where(CropListingModel.id == listing_id))
    listing = res.scalar_one_or_none()
    if not listing:
        raise NotFoundException("Crop listing")

    if listing.farmer_id != farmer_id:
        raise ForbiddenException("You do not have permission to delete this listing.")

    await db.delete(listing)
    await db.commit()
    logger.info(f"🗑️ Crop Listing deleted ID: {listing_id} by farmer: {farmer_id}")
    return True
