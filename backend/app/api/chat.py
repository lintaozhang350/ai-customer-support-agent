from fastapi import APIRouter

from app.schemas.chat import ChatHistoryMessage, ChatRequest, ChatResponse
from app.services.agent_service import handle_chat
from app.services.conversation_service import list_chat_messages, save_chat_exchange

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    response = handle_chat(request)
    save_chat_exchange(
        conversation_id=request.conversation_id or "default",
        user_id=request.user_id,
        customer_message=request.message,
        agent_response=response,
    )
    return response


@router.get("/history/{conversation_id}", response_model=list[ChatHistoryMessage])
def read_chat_history(conversation_id: str) -> list[ChatHistoryMessage]:
    return list_chat_messages(conversation_id)
