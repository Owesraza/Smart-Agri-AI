"""Requirements router — /api/v1/requirements"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import marketplace_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/requirements", tags=["Buyer Requirements"])


class BuyerRequirementRequest(BaseModel):
    crop_name: str = Field(..., example="Wheat")
    quantity_required: float = Field(..., gt=0, example=100.0)
    offered_price: float = Field(..., gt=0, example=2250.0)
    required_before: Optional[date] = Field(default=None)
    preferred_quality: Optional[str] = Field(default="Grade A")
    preferred_district: Optional[str] = Field(default="Nashik")
    delivery_location: Optional[str] = Field(default="Nashik APMC Yard")
    notes: Optional[str] = Field(default=None)


class BuyerRequirementUpdate(BaseModel):
    crop_name: Optional[str] = None
    quantity_required: Optional[float] = Field(None, gt=0)
    offered_price: Optional[float] = Field(None, gt=0)
    preferred_quality: Optional[str] = None
    preferred_district: Optional[str] = None
    delivery_location: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


@router.post("", summary="Buyer posts buying requirement (Triggers AI Matcher)", status_code=201)
@router.post("/", summary="Buyer posts buying requirement (Triggers AI Matcher)", status_code=201)
async def create_requirement(
    data: BuyerRequirementRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    res = await marketplace_service.create_buyer_requirement(db, current_user["id"], data.model_dump())
    return success_response(res, "Buyer requirement posted. AI Matcher generated top matches.")


@router.get("/", summary="List buying requirements (Public / Marketplace)")
async def list_requirements(
    crop: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    status: str = Query("Open"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    res = await marketplace_service.get_buyer_requirements(
        db=db, crop=crop, district=district, status=status, page=page, limit=limit
    )
    return success_response(res["requirements"], "Requirements fetched", res["pagination"])


@router.get("/my", summary="Get current buyer's own requirements")
async def get_my_requirements(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    reqs = await marketplace_service.get_my_buyer_requirements(db, current_user["id"])
    return success_response(reqs, "Buyer's requirements fetched")


@router.put("/{req_id}", summary="Update buyer requirement")
async def edit_requirement(
    req_id: str,
    data: BuyerRequirementUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    req = await marketplace_service.update_buyer_requirement(db, current_user["id"], req_id, data.model_dump(exclude_unset=True))
    return success_response(req, "Requirement updated")


@router.delete("/{req_id}", summary="Delete buyer requirement")
async def remove_requirement(
    req_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await marketplace_service.delete_buyer_requirement(db, current_user["id"], req_id)
    return success_response(None, "Requirement deleted")
