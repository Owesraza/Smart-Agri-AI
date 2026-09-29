"""Auth router — /api/v1/auth"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.user import UserRegister, UserLogin, ForgotPassword, ResetPassword, RefreshTokenRequest
from app.services import auth_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", summary="Register a new user")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, data)
    return success_response(user, "Account created successfully")


@router.post("/login", summary="Login with email and password")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await auth_service.login_user(db, data)
    return success_response(result, "Login successful")


@router.post("/refresh", summary="Get new access token using refresh token")
async def refresh(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    tokens = await auth_service.refresh_access_token(db, data.refresh_token)
    return success_response(tokens, "Token refreshed")


@router.post("/logout", summary="Logout and invalidate refresh token")
async def logout(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    await auth_service.logout_user(db, data.refresh_token)
    return success_response(None, "Logged out successfully")


@router.post("/forgot-password", summary="Request password reset token")
async def forgot_password(data: ForgotPassword, db: AsyncSession = Depends(get_db)):
    token = await auth_service.forgot_password(db, data.email)
    return success_response({"reset_token": token}, "Password reset token generated")


@router.post("/reset-password", summary="Reset password with token")
async def reset_password(data: ResetPassword, db: AsyncSession = Depends(get_db)):
    await auth_service.reset_password(db, data.token, data.new_password)
    return success_response(None, "Password reset successfully")
