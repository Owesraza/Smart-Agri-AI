"""
Chat Manager — WebSockets Real-Time Chat & Message Persistence.
"""
import logging
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from app.models.sql_models import ConversationModel, MessageModel, UserModel
from app.utils.helpers import serialize_doc, serialize_list

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Tracks active WebSocket connections per user_id."""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"🔌 WebSocket connected for user {user_id}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"🔌 WebSocket disconnected for user {user_id}")

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))


ws_manager = ConnectionManager()


async def get_or_create_conversation(
    db: AsyncSession,
    user1_id: str,
    user2_id: str,
    listing_id: Optional[str] = None,
    offer_id: Optional[str] = None,
) -> Dict:
    """Retrieve existing conversation between 2 users or create a new one."""
    stmt = select(ConversationModel).where(
        or_(
            and_(ConversationModel.user1_id == user1_id, ConversationModel.user2_id == user2_id),
            and_(ConversationModel.user1_id == user2_id, ConversationModel.user2_id == user1_id),
        )
    )
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()

    if not conv:
        now = datetime.now(timezone.utc)
        conv = ConversationModel(
            user1_id=user1_id,
            user2_id=user2_id,
            listing_id=listing_id,
            offer_id=offer_id,
            last_message="Conversation started",
            updated_at=now,
        )
        db.add(conv)
        await db.commit()
        await db.refresh(conv)

    return serialize_doc(conv)


async def send_chat_message(
    db: AsyncSession,
    conversation_id: str,
    sender_id: str,
    receiver_id: str,
    text: str,
) -> Dict:
    """Store chat message in DB and broadcast via WebSockets."""
    now = datetime.now(timezone.utc)
    msg = MessageModel(
        conversation_id=conversation_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        text=text,
        is_read=False,
        created_at=now,
    )
    db.add(msg)

    # Update conversation last message
    res_c = await db.execute(select(ConversationModel).where(ConversationModel.id == conversation_id))
    conv = res_c.scalar_one_or_none()
    if conv:
        conv.last_message = text
        conv.updated_at = now

    await db.commit()
    await db.refresh(msg)

    payload = {
        "id": msg.id,
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "text": text,
        "created_at": now.isoformat(),
    }

    # Send WebSocket message if receiver is online
    await ws_manager.send_personal_message(payload, receiver_id)

    return payload


async def get_conversation_messages(db: AsyncSession, conversation_id: str, limit: int = 50) -> List[Dict]:
    """Retrieve message history for a conversation."""
    stmt = (
        select(MessageModel)
        .where(MessageModel.conversation_id == conversation_id)
        .order_by(MessageModel.created_at.asc())
        .limit(limit)
    )
    res = await db.execute(stmt)
    msgs = res.scalars().all()
    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "text": m.text,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in msgs
    ]
