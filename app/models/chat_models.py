from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    mode: str = "friendly_ai"

class SaveChatRequest(BaseModel):
    messages: List[Message]

