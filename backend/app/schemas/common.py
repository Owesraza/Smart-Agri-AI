"""Pydantic schemas shared across all modules."""
from pydantic import BaseModel, Field
from typing import Any, Optional
from bson import ObjectId


class PyObjectId(str):
    """Custom Pydantic type for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return str(v)


class APIResponse(BaseModel):
    """Standard API response envelope."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None
    meta: Optional[dict] = None


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool
