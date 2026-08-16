from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.intent_classifier import build_placeholder_answer, classify_message

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    intent_result = classify_message(request.message)
    answer = build_placeholder_answer(intent_result)

    return ChatResponse(answer=answer, intent_result=intent_result)
