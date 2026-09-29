"""User Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.constants.constants import UserRole, INDIAN_STATES, LANGUAGES
from app.utils.validators import validate_phone, validate_password_strength


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    mobile_number: str = Field(..., description="10-digit Indian mobile number")
    email: EmailStr
    password: str = Field(..., min_length=8)
    village: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None)
    farm_size: Optional[float] = Field(None, gt=0, description="Farm size in acres")
    preferred_language: Optional[str] = Field("Hindi")
    role: Optional[str] = Field(UserRole.FARMER)

    @field_validator("mobile_number")
    @classmethod
    def check_phone(cls, v):
        return validate_phone(v)

    @field_validator("password")
    @classmethod
    def check_password(cls, v):
        return validate_password_strength(v)

    @field_validator("role")
    @classmethod
    def check_role(cls, v):
        v_norm = v.lower() if v else UserRole.FARMER
        if v_norm not in UserRole.ALL:
            raise ValueError(f"Role must be one of: {UserRole.ALL}")
        return v_norm


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    mobile_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    farm_size: Optional[float] = Field(None, gt=0)
    preferred_language: Optional[str] = None

    @field_validator("mobile_number", "whatsapp_number")
    @classmethod
    def check_phone(cls, v):
        return validate_phone(v) if v else v


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def check_new_password(cls, v):
        return validate_password_strength(v)


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v):
        return validate_password_strength(v)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    full_name: str
    mobile_number: str
    email: str
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    farm_size: Optional[float] = None
    preferred_language: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
