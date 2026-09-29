"""Pydantic Schemas for Crop Listings"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class CropListingCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    crop: str = Field(..., example="Wheat", description="Name of the crop")
    quantity: float = Field(..., gt=0, example=100.0, description="Available quantity in Quintals")
    expected_price: float = Field(..., gt=0, example=2300.0, description="Expected price per Quintal (₹)")
    harvest_date: Optional[date] = Field(default=None, description="Harvest date")
    quality_grade: Optional[str] = Field(default="Grade A", description="Quality grade e.g. Grade A, Grade B")
    location: Optional[str] = Field(default="Nashik APMC Yard", description="Mandi location or village")
    available_until: Optional[date] = Field(default=None, description="Expiration date for listing")
    photo_url: Optional[str] = Field(default=None, description="URL of crop photo")
    plot_id: Optional[str] = Field(default=None, description="Associated plot ID")
    advance_days: Optional[int] = Field(default=0, description="Pre-harvest booking lead time in days")
    status: Optional[str] = Field(default="ACTIVE", description="ACTIVE, RESERVED, SOLD")


class CropListingUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    crop: Optional[str] = Field(default=None)
    quantity: Optional[float] = Field(default=None, gt=0)
    expected_price: Optional[float] = Field(default=None, gt=0)
    harvest_date: Optional[date] = Field(default=None)
    quality_grade: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    available_until: Optional[date] = Field(default=None)
    photo_url: Optional[str] = Field(default=None)
    plot_id: Optional[str] = Field(default=None)
    advance_days: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None, description="ACTIVE, RESERVED, SOLD")


class CropListingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    farmer_id: str
    plot_id: Optional[str] = None
    crop: str
    quantity: float
    expected_price: float
    harvest_date: Optional[date] = None
    quality_grade: str
    location: Optional[str] = None
    available_until: Optional[date] = None
    photo_url: Optional[str] = None
    advance_days: Optional[int] = 0
    discount_pct: Optional[float] = 0.0
    discounted_price: Optional[float] = None
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
