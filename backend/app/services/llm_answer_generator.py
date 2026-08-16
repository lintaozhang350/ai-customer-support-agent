import json
from typing import Any
from urllib import error, request

from app.core.settings import get_settings
from app.schemas.chat import ChatHistoryMessage, IntentResult


def generate_answer_with_llm(
    user_message: str,
    default_answer: str,
    intent_result: IntentResult,
    tool_used: str | None,
    tool_result: dict[str, Any] | list[dict[str, Any]] | None,
    conversation_history: list[ChatHistoryMessage] | None = None,
) -> str | None:
    settings = get_settings()
    if not settings.enable_llm_answer_generation or not settings.openai_api_key:
        return None

    payload = {
        "model": settings.openai_model,
        "instructions": _build_system_prompt(),
        "input": _build_input(
            user_message=user_message,
            default_answer=default_answer,
            intent_result=intent_result,
            tool_used=tool_used,
            tool_result=tool_result,
            conversation_history=conversation_history or [],
        ),
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
        cleaned_text = output_text.strip()
        return cleaned_text or None
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def _build_system_prompt() -> str:
    return """
You are a customer support reply writer for an ecommerce help desk.
Rewrite the provided fallback answer so it sounds natural, concise, and professional.

Rules:
- Keep the answer factually consistent with the supplied tool result.
- Do not invent policies, dates, tracking numbers, products, or order details.
- If the fallback answer already refuses a privacy-unsafe request, keep the refusal firm.
- Sound like a store support team member, not a generic AI chatbot.
- Do not say "virtual assistant" or over-explain your role.
- If the user asks who you are or what you can do, answer briefly and redirect to the support tasks you can help with.
- Do not mention internal fields like intent, tool_used, confidence, or JSON.
- Return plain text only.
""".strip()


def _build_input(
    user_message: str,
    default_answer: str,
    intent_result: IntentResult,
    tool_used: str | None,
    tool_result: dict[str, Any] | list[dict[str, Any]] | None,
    conversation_history: list[ChatHistoryMessage],
) -> str:
    recent_history = conversation_history[-4:]
    history_lines = [
        f"{history_message.role}: {history_message.text}"
        for history_message in recent_history
    ]
    history_block = "\n".join(history_lines) if history_lines else "(no prior messages)"

    return "\n\n".join(
        [
            f"Conversation history:\n{history_block}",
            f"User message:\n{user_message}",
            f"Fallback answer:\n{default_answer}",
            f"Intent result:\n{intent_result.model_dump_json()}",
            f"Tool used:\n{tool_used or 'none'}",
            f"Tool result:\n{json.dumps(tool_result, ensure_ascii=True)}",
        ]
    )


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
