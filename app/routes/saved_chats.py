from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.chat_models import SaveChatRequest


router = APIRouter()

saved_chats = []

@router.post("/save-chat")
async def save_chat(data: SaveChatRequest):
    chat_id = len(saved_chats) + 1
    saved_chats.append({
        "id": chat_id,
        "messages": data.messages,
        "created_at": datetime.utcnow().isoformat()
    })
    return {"message": "Chat saved successfully", "id": chat_id}

@router.get("/saved-chats")
async def get_saved_chats():
    return saved_chats
