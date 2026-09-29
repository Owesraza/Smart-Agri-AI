"""Chat router — /api/v1/chat & WebSockets /ws/chat/{conversation_id}"""
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.database.connection import get_db, AsyncSessionLocal
from app.dependencies.auth import get_current_active_user
from app.services import chat_manager
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/chat", tags=["Real-Time Chat & WebSockets"])


class SendMessageRequest(BaseModel):
    conversation_id: str = Field(..., example="conv_123")
    receiver_id: str = Field(..., example="user_456")
    text: str = Field(..., example="Hello, is the Wheat ready for pickup tomorrow?")


@router.get("/messages", summary="Get message history for a conversation")
async def get_messages_endpoint(
    conversation_id: str = Query(...),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    msgs = await chat_manager.get_conversation_messages(db, conversation_id)
    return success_response(msgs, "Chat history fetched")


@router.post("/send", summary="Send a chat message (HTTP & WebSocket broadcast)")
async def send_message_endpoint(
    data: SendMessageRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    msg = await chat_manager.send_chat_message(
        db=db,
        conversation_id=data.conversation_id,
        sender_id=current_user["id"],
        receiver_id=data.receiver_id,
        text=data.text,
    )
    return success_response(msg, "Message sent")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket connection endpoint for real-time chat & notifications."""
    await chat_manager.ws_manager.connect(user_id, websocket)
    try:
        while True:
            data_text = await websocket.receive_text()
            # Echo back typing status / keepalive
            await websocket.send_text(f'{{"type": "ack", "received": {data_text}}}')
    except WebSocketDisconnect:
        chat_manager.ws_manager.disconnect(user_id)
