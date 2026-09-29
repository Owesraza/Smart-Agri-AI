"""Ratings router — /api/v1/ratings"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import rating_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/ratings", tags=["Ratings & Reviews"])


class RatingCreateRequest(BaseModel):
    to_user_id: str = Field(..., example="user_456")
    rating: float = Field(..., ge=1.0, le=5.0, example=5.0)
    deal_id: Optional[str] = Field(default=None, example="deal_123")
    review: Optional[str] = Field(default="Excellent crop quality and prompt payment!")


@router.post("", summary="Submit star rating & review for a deal", status_code=201)
@router.post("/", summary="Submit star rating & review for a deal", status_code=201)
async def submit_rating(
    data: RatingCreateRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    rate = await rating_service.create_rating(
        db=db,
        from_user_id=current_user["id"],
        deal_id=data.deal_id,
        to_user_id=data.to_user_id,
        rating=data.rating,
        review=data.review,
    )
    return success_response(rate, "Rating submitted successfully")


@router.get("/{user_id}", summary="Get user's average rating and review count")
async def get_user_rating(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    stats = await rating_service.get_user_average_rating(db, user_id)
    return success_response(stats, "User rating stats fetched")
