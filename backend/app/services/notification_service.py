"""
Notification Service — Real-time notifications for Farmers & Buyers.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.sql_models import NotificationModel
from app.utils.helpers import serialize_list

logger = logging.getLogger(__name__)


async def create_notification(
    db: AsyncSession,
    user_id: str,
    title: str,
    message: str,
    type_: str = "Info"
) -> Dict:
    """Create a new notification for a user."""
    notif = NotificationModel(
        user_id=user_id,
        title=title,
        message=message,
        type=type_,
        is_read=False,
        created_at=datetime.now(timezone.utc),
    )
    db.add(notif)
    await db.commit()
    await db.refresh(notif)
    logger.info(f"🔔 Notification sent to user {user_id}: {title}")
    return {
        "id": notif.id,
        "user_id": notif.user_id,
        "title": notif.title,
        "message": notif.message,
        "type": notif.type,
        "is_read": notif.is_read,
        "created_at": notif.created_at.isoformat(),
    }


async def get_user_notifications(db: AsyncSession, user_id: str, unread_only: bool = False) -> List[Dict]:
    """Retrieve notifications for a user."""
    stmt = select(NotificationModel).where(NotificationModel.user_id == user_id)
    if unread_only:
        stmt = stmt.where(NotificationModel.is_read == False)
    stmt = stmt.order_by(NotificationModel.created_at.desc()).limit(50)
    res = await db.execute(stmt)
    notifs = res.scalars().all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in notifs
    ]


async def mark_notifications_read(db: AsyncSession, user_id: str, notif_id: str = None) -> bool:
    """Mark notification(s) as read."""
    if notif_id:
        stmt = update(NotificationModel).where(
            NotificationModel.id == notif_id,
            NotificationModel.user_id == user_id
        ).values(is_read=True)
    else:
        stmt = update(NotificationModel).where(
            NotificationModel.user_id == user_id
        ).values(is_read=True)
    await db.execute(stmt)
    await db.commit()
    return True
