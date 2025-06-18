from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.chat_models import ChatRequest
from app.services.prompt_service import get_mistral_response

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    stream = get_mistral_response(chat_request)
    return StreamingResponse(stream, media_type="text/plain")