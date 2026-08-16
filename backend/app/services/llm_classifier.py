import json
from typing import Any
from urllib import error, request

from app.core.settings import get_settings
from app.schemas.chat import ChatHistoryMessage, IntentResult


def classify_message_with_llm(
    message: str,
    conversation_history: list[ChatHistoryMessage] | None = None,
) -> IntentResult | None:
    settings = get_settings()
    if not settings.enable_llm_classifier or not settings.openai_api_key:
        return None

    payload = {
        "model": settings.openai_model,
        "instructions": _build_system_prompt(),
        "input": _build_input(message, conversation_history or []),
    }

    http_request = request.Request(
        url=f"{settings.openai_base_url.rstrip('/')}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=20) as response:
            response_body = response.read().decode("utf-8")
    except (error.HTTPError, error.URLError, TimeoutError):
        return None

    try:
        response_data = json.loads(response_body)
        output_text = _extract_output_text(response_data)
        output_json = _extract_json_object(output_text)
        return IntentResult.model_validate(output_json)
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return None


def _build_system_prompt() -> str:
    return """
You are an intent classifier for an ecommerce customer support assistant.
Return JSON only.

Allowed intents:
- order_status
- return_policy
- shipping_policy
- warranty_policy
- product_recommendation
- complaint
- human_escalation
- unsafe_private_request
- general_question

Allowed suggested_action values:
- lookup_order
- search_policy
- search_products
- create_support_ticket
- refuse_request
- answer_generally

Return an object with this exact shape:
{
  "intent": string,
  "confidence": number,
  "entities": {
    "order_id": number or null,
    "category": string or null,
    "budget": number or null,
    "keyword": string or null
  },
  "suggested_action": string
}

Infer order_id, category, budget, and keyword when possible.
If the request asks for another customer's private information, use unsafe_private_request.
""".strip()


def _build_input(
    message: str,
    conversation_history: list[ChatHistoryMessage],
) -> str:
    recent_history = conversation_history[-6:]
    history_lines = [
        f"{history_message.role}: {history_message.text}"
        for history_message in recent_history
    ]

    history_block = "\n".join(history_lines) if history_lines else "(no prior messages)"
    return f"Conversation history:\n{history_block}\n\nCurrent user message:\n{message}"


def _extract_output_text(response_data: dict[str, Any]) -> str:
    output_items = response_data["output"]
    for output_item in output_items:
        if output_item.get("type") != "message":
            continue

        for content_item in output_item.get("content", []):
            text_value = content_item.get("text")
            if isinstance(text_value, str) and text_value.strip():
                return text_value

    raise KeyError("No text content found in LLM response")


def _extract_json_object(output_text: str) -> dict[str, Any]:
    start_index = output_text.find("{")
    end_index = output_text.rfind("}")

    if start_index == -1 or end_index == -1 or end_index <= start_index:
        raise ValueError("No JSON object found in output text")

    return json.loads(output_text[start_index : end_index + 1])
