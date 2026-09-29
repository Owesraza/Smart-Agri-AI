"""Users router — /api/v1/users"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.user import UserUpdate, PasswordChange
from app.services import user_service
from app.dependencies.auth import get_current_active_user, require_admin
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", summary="Get current user profile")
async def get_me(current_user: dict = Depends(get_current_active_user)):
    return success_response(current_user, "Profile fetched")


@router.patch("/me", summary="Update current user profile (PATCH)")
@router.put("/me", summary="Update current user profile (PUT)")
async def update_me(
    data: UserUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.update_user(db, current_user["id"], data)
    return success_response(user, "Profile updated")


@router.patch("/me/password", summary="Change password")
async def change_password(
    data: PasswordChange,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await user_service.change_password(db, current_user["id"], data)
    return success_response(None, "Password changed successfully")


@router.get("/", summary="List all users (admin only)", dependencies=[Depends(require_admin)])
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await user_service.list_users(db, page, limit)
    return success_response(result["users"], "Users fetched", result["pagination"])


@router.get("/{user_id}", summary="Get user by ID (admin only)", dependencies=[Depends(require_admin)])
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_id(db, user_id)
    return success_response(user, "User fetched")


@router.delete("/{user_id}", summary="Delete user (admin only)", dependencies=[Depends(require_admin)])
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    await user_service.delete_user(db, user_id)
    return success_response(None, "User deleted")
