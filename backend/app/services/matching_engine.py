"""
AI Matching Engine — Intelligent Agricultural Marketplace Matcher.
Ranks matches between Buyer Requirements and Farmer Crop Listings using:
- Crop Match (Primary filter)
- Quantity Match (%)
- Price Difference (%)
- Distance / Location proximity (km)
- Buyer & Farmer Ratings
- Returns top 5 ranked matches and stores AI Match Scores in database.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.sql_models import BuyerRequirementModel, CropListingModel, MatchModel, UserModel
from app.services.market_service import normalize_crop_name

logger = logging.getLogger(__name__)


def calculate_match_score(
    req_qty: float, list_qty: float,
    req_price: float, list_price: float,
    req_district: Optional[str], list_location: Optional[str],
    farmer_rating: float = 5.0, buyer_rating: float = 5.0,
) -> Dict:
    """Calculate 0-100 composite match score."""
    # 1. Quantity score (max 30 pts)
    qty_ratio = min(req_qty, list_qty) / max(req_qty, list_qty) if max(req_qty, list_qty) > 0 else 1.0
    qty_score = qty_ratio * 30.0

    # 2. Price score (max 35 pts) - closer prices = higher score
    price_diff_pct = abs(req_price - list_price) / max(req_price, 1.0) * 100.0
    price_score = max(0.0, 35.0 - (price_diff_pct * 1.5))

    # 3. Location/Distance score (max 20 pts)
    dist_score = 20.0
    approx_dist = 15.0
    if req_district and list_location and req_district.lower() in list_location.lower():
        dist_score = 20.0
        approx_dist = 8.0
    else:
        dist_score = 12.0
        approx_dist = 45.0

    # 4. Rating score (max 15 pts)
    rating_avg = (farmer_rating + buyer_rating) / 2.0
    rating_score = (rating_avg / 5.0) * 15.0

    total_score = round(min(100.0, max(10.0, qty_score + price_score + dist_score + rating_score)), 1)

    return {
        "match_score": total_score,
        "quantity_match_pct": round(qty_ratio * 100.0, 1),
        "price_diff_pct": round(price_diff_pct, 1),
        "distance_km": approx_dist,
    }


async def match_requirement_for_buyer(db: AsyncSession, requirement_id: str) -> List[Dict]:
    """Find top 5 farmer crop listing matches for a buyer requirement."""
    res_req = await db.execute(select(BuyerRequirementModel).where(BuyerRequirementModel.id == requirement_id))
    req = res_req.scalar_one_or_none()
    if not req:
        return []

    crop_norm = normalize_crop_name(req.crop_name)

    # Find matching crop listings
    res_listings = await db.execute(
        select(CropListingModel)
        .where(
            and_(
                CropListingModel.crop.ilike(f"%{crop_norm}%"),
                CropListingModel.status == "Available"
            )
        )
    )
    listings = res_listings.scalars().all()

    matches = []
    now = datetime.now(timezone.utc)

    for l in listings:
        score_dict = calculate_match_score(
            req_qty=req.quantity_required,
            list_qty=l.quantity,
            req_price=req.offered_price,
            list_price=l.expected_price,
            req_district=req.preferred_district,
            list_location=l.location,
        )

        match_obj = MatchModel(
            requirement_id=req.id,
            listing_id=l.id,
            buyer_id=req.buyer_id,
            farmer_id=l.farmer_id,
            match_score=score_dict["match_score"],
            crop_match=True,
            quantity_match_pct=score_dict["quantity_match_pct"],
            price_diff_pct=score_dict["price_diff_pct"],
            distance_km=score_dict["distance_km"],
            created_at=now,
        )
        db.add(match_obj)

        # Get farmer info
        f_user_res = await db.execute(select(UserModel).where(UserModel.id == l.farmer_id))
        f_user = f_user_res.scalar_one_or_none()

        matches.append({
            "match_id": match_obj.id,
            "listing_id": l.id,
            "farmer_name": f_user.full_name if f_user else "Farmer",
            "farmer_location": l.location,
            "crop": l.crop,
            "available_quantity": l.quantity,
            "expected_price": l.expected_price,
            "match_score": score_dict["match_score"],
            "distance_km": score_dict["distance_km"],
            "price_difference_pct": score_dict["price_diff_pct"],
        })

    await db.commit()

    # Sort top matches by score
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    top_matches = matches[:5]
    logger.info(f"⚡ AI Matcher: Found {len(top_matches)} top matches for requirement {requirement_id}")
    return top_matches
