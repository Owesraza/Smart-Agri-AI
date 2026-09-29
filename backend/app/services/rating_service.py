"""
Rating Service — Star Ratings & Reviews for Farmers & Buyers.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.sql_models import RatingModel, DealModel, UserModel, PurchaseRequestModel
from app.utils.exceptions import NotFoundException, ForbiddenException, BadRequestException, ConflictException
from app.utils.helpers import serialize_doc

logger = logging.getLogger(__name__)


async def create_rating(
    db: AsyncSession,
    from_user_id: str,
    deal_id: Optional[str],
    to_user_id: str,
    rating: float,
    review: str = None
) -> Dict:
    """Submit a star rating (1-5) and review for a completed deal or interaction."""
    if not (1.0 <= float(rating) <= 5.0):
        raise BadRequestException("Rating must be between 1.0 and 5.0 stars.")

    # Validate target user exists
    res_u = await db.execute(select(UserModel).where(UserModel.id == to_user_id))
    if not res_u.scalar_one_or_none():
        raise NotFoundException("Target user")

    actual_deal_id = deal_id or f"deal_{from_user_id[:8]}_{to_user_id[:8]}"

    # Prevent duplicate rating for the same deal by the same user
    res_dup = await db.execute(
        select(RatingModel).where(
            RatingModel.from_user_id == from_user_id,
            RatingModel.deal_id == actual_deal_id
        )
    )
    if res_dup.scalar_one_or_none():
        raise ConflictException("You have already submitted a rating for this deal.")

    now = datetime.now(timezone.utc)
    
    rate_obj = RatingModel(
        deal_id=actual_deal_id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        rating=float(rating),
        review=review or "Verified transaction feedback.",
        created_at=now,
    )
    db.add(rate_obj)
    await db.commit()
    await db.refresh(rate_obj)

    logger.info(f"⭐ Rating {rating} stars submitted from {from_user_id} to {to_user_id}")
    return serialize_doc(rate_obj)


async def get_user_average_rating(db: AsyncSession, user_id: str) -> Dict:
    """Calculate overall average rating score and review count for a user."""
    stmt = (
        select(
            func.coalesce(func.avg(RatingModel.rating), 5.0).label("avg_rating"),
            func.count(RatingModel.id).label("total_reviews")
        )
        .where(RatingModel.to_user_id == user_id)
    )
    res = await db.execute(stmt)
    avg_r, count = res.fetchone()

    return {
        "user_id": user_id,
        "average_rating": round(float(avg_r or 5.0), 1),
        "total_reviews": int(count or 0),
    }
