"""Listings Router — /api/v1/listings"""
from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.schemas.listing_schemas import CropListingCreate, CropListingUpdate
from app.services import listing_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/listings", tags=["Crop Listings"])


@router.post("", summary="Create a new Crop Listing", status_code=status.HTTP_201_CREATED)
@router.post("/", summary="Create a new Crop Listing", status_code=status.HTTP_201_CREATED)
async def create_listing(
    data: CropListingCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new crop listing for the authenticated farmer."""
    listing = await listing_service.create_crop_listing(db, current_user["id"], data.model_dump())
    return success_response(listing, "Crop listing created successfully")


@router.get("/my", summary="Get authenticated farmer's own listings")
async def get_my_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all crop listings owned by the logged-in farmer."""
    res = await listing_service.get_farmer_own_listings(db, current_user["id"], page=page, limit=limit)
    return success_response(res["listings"], "Farmer listings fetched", res["pagination"])


@router.get("", summary="Search and list active crop listings for buyers")
@router.get("/", summary="Search and list active crop listings for buyers")
async def list_active_listings(
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    location: Optional[str] = Query(None, description="Filter by location/mandi"),
    min_price: Optional[float] = Query(None, description="Minimum expected price"),
    max_price: Optional[float] = Query(None, description="Maximum expected price"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all ACTIVE crop listings available in the marketplace."""
    res = await listing_service.get_all_active_listings(
        db=db,
        crop=crop,
        location=location,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit,
    )
    return success_response(res["listings"], "Active listings fetched", res["pagination"])


@router.get("/{id}", summary="Get crop listing by ID")
async def get_listing_by_id(
    id: str = Path(..., description="Crop Listing ID"),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve details for a single crop listing."""
    listing = await listing_service.get_listing_by_id(db, id)
    return success_response(listing, "Listing details fetched")


@router.put("/{id}", summary="Update a crop listing")
async def update_listing(
    data: CropListingUpdate,
    id: str = Path(..., description="Crop Listing ID"),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a crop listing (Secured: Only owner farmer can update)."""
    listing = await listing_service.update_crop_listing(db, current_user["id"], id, data.model_dump(exclude_unset=True))
    return success_response(listing, "Crop listing updated successfully")


@router.delete("/{id}", summary="Delete a crop listing")
async def delete_listing(
    id: str = Path(..., description="Crop Listing ID"),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a crop listing (Secured: Only owner farmer can delete)."""
    await listing_service.delete_crop_listing(db, current_user["id"], id)
    return success_response(None, "Crop listing deleted successfully")
