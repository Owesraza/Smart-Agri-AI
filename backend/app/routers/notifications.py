"""Notifications router — /api/v1/notifications"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import notification_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


@router.get("", summary="Get user's real-time notifications")
@router.get("/", summary="Get user's real-time notifications")
async def list_notifications(
    unread_only: bool = Query(False),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    notifs = await notification_service.get_user_notifications(db, current_user["id"], unread_only)
    return success_response(notifs, "Notifications fetched")


@router.patch("/read", summary="Mark notifications as read")
async def mark_read_endpoint(
    notif_id: Optional[str] = Query(None, description="Leave blank to mark all as read"),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await notification_service.mark_notifications_read(db, current_user["id"], notif_id)
    return success_response(None, "Notifications marked as read")
