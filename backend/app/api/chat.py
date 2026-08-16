from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent_service import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return handle_chat(request)
