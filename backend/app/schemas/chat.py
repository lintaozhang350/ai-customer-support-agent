from typing import Any, Literal
from datetime import datetime

from pydantic import BaseModel, Field


Intent = Literal[
    "order_status",
    "return_policy",
    "shipping_policy",
    "warranty_policy",
    "product_recommendation",
    "complaint",
    "human_escalation",
    "unsafe_private_request",
    "general_question",
]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    user_id: int | None = None
    conversation_id: str | None = None


class ExtractedEntities(BaseModel):
    order_id: int | None = None
    category: str | None = None
    budget: float | None = None
    keyword: str | None = None


class IntentResult(BaseModel):
    intent: Intent
    confidence: float
    entities: ExtractedEntities
    suggested_action: str


class ChatResponse(BaseModel):
    answer: str
    intent_result: IntentResult
    tool_used: str | None = None
    tool_result: dict[str, Any] | list[dict[str, Any]] | None = None


class ChatHistoryMessage(BaseModel):
    id: int
    conversation_id: str
    user_id: int | None = None
    role: Literal["customer", "agent"]
    text: str
    metadata: dict[str, Any] | None = None
    created_at: datetime


class ConversationSummary(BaseModel):
    conversation_id: str
    user_id: int | None = None
    preview: str
    message_count: int
    last_message_at: datetime
