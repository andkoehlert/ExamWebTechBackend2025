from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    mode: str = "friendly_ai"
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None


class SaveChatRequest(BaseModel):
    messages: List[Message]

