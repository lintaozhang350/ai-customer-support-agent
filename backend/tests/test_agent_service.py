from datetime import datetime

from app.schemas.chat import ChatHistoryMessage, ChatRequest
from app.services import agent_service
from app.services.agent_service import handle_chat
from app.services.intent_classifier import classify_message


def test_classifier_extracts_order_id() -> None:
    result = classify_message("Where is my order 1001?")

    assert result.intent == "order_status"
    assert result.entities.order_id == 1001
    assert result.suggested_action == "lookup_order"


def test_classifier_extracts_product_preferences() -> None:
    result = classify_message("Recommend a budget keyboard under $50")

    assert result.intent == "product_recommendation"
    assert result.entities.category == "keyboard"
    assert result.entities.budget == 50
    assert result.entities.keyword == "keyboard"


def test_handle_chat_returns_helpful_fallback_for_general_question() -> None:
    response = handle_chat(ChatRequest(message="hello"))

    assert response.intent_result.intent == "general_question"
    assert response.tool_used is None
    assert "order, product, policy, or issue" in response.answer


def test_handle_chat_handles_missing_order_number() -> None:
    response = handle_chat(ChatRequest(message="track my order"))

    assert response.intent_result.intent == "order_status"
    assert response.tool_used == "get_order_status"
    assert response.tool_result is None
    assert "order number" in response.answer


def test_handle_chat_uses_conversation_context_for_order_follow_up() -> None:
    history = [
        ChatHistoryMessage(
            id=1,
            conversation_id="demo",
            user_id=1,
            role="customer",
            text="Where is my order 1001?",
            metadata=None,
            created_at="2026-08-16T17:00:00",
        )
    ]

    response = handle_chat(
        ChatRequest(message="When will it arrive?"),
        conversation_history=history,
    )

    assert response.intent_result.intent == "order_status"
    assert response.intent_result.entities.order_id == 1001
    assert response.tool_used == "get_order_status"


def test_handle_chat_uses_conversation_context_for_product_follow_up() -> None:
    history = [
        ChatHistoryMessage(
            id=1,
            conversation_id="demo",
            user_id=1,
            role="customer",
            text="Recommend a budget keyboard under $50",
            metadata=None,
            created_at="2026-08-16T17:00:00",
        )
    ]

    response = handle_chat(
        ChatRequest(message="Anything cheaper?"),
        conversation_history=history,
    )

    assert response.intent_result.intent == "product_recommendation"
    assert response.intent_result.entities.category == "keyboard"
    assert response.tool_used == "search_products"


def test_handle_chat_falls_back_when_llm_classifier_returns_none(monkeypatch) -> None:
    monkeypatch.setattr(agent_service, "classify_message_with_llm", lambda *_args, **_kwargs: None)

    response = handle_chat(ChatRequest(message="Where is my order 1001?"))

    assert response.intent_result.intent == "order_status"
    assert response.tool_used == "get_order_status"


def test_handle_chat_uses_llm_classifier_when_available(monkeypatch) -> None:
    llm_result = classify_message("Recommend a budget keyboard under $50")
    history = [
        ChatHistoryMessage(
            id=1,
            conversation_id="demo",
            user_id=1,
            role="customer",
            text="I need a keyboard",
            metadata=None,
            created_at=datetime(2026, 8, 16, 17, 0, 0),
        )
    ]

    monkeypatch.setattr(
        agent_service,
        "classify_message_with_llm",
        lambda *_args, **_kwargs: llm_result,
    )

    response = handle_chat(
        ChatRequest(message="Anything under $50?"),
        conversation_history=history,
    )

    assert response.intent_result.intent == "product_recommendation"
    assert response.intent_result.entities.category == "keyboard"
    assert response.tool_used == "search_products"
