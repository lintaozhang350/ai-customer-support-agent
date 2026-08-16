import re

from app.schemas.chat import ExtractedEntities, Intent, IntentResult


ORDER_ID_PATTERN = re.compile(r"\b(?:order\s*#?|#)?(\d{4,})\b", re.IGNORECASE)
BUDGET_PATTERN = re.compile(r"(?:under|below|less than|max|budget)\s*\$?(\d+(?:\.\d+)?)", re.IGNORECASE)


CATEGORY_KEYWORDS = {
    "keyboard": "keyboard",
    "mouse": "mouse",
    "headphones": "headphones",
    "headphone": "headphones",
    "hub": "accessory",
    "adapter": "accessory",
    "monitor": "monitor",
}


def classify_message(message: str) -> IntentResult:
    normalized = message.lower()
    entities = ExtractedEntities(
        order_id=_extract_order_id(message),
        category=_extract_category(normalized),
        budget=_extract_budget(message),
        keyword=_extract_keyword(normalized),
    )

    if _contains_any(normalized, ["another customer", "customer address", "someone else's", "private info"]):
        return _result("unsafe_private_request", 0.95, entities, "refuse_request")

    if _contains_any(normalized, ["manager", "human", "representative", "agent", "supervisor"]):
        return _result("human_escalation", 0.9, entities, "create_support_ticket")

    if _contains_any(normalized, ["damaged", "broken", "missing", "angry", "frustrated", "complaint"]):
        return _result("complaint", 0.88, entities, "create_support_ticket")

    if entities.order_id is not None or _contains_any(normalized, ["where is my order", "track my order", "order status"]):
        return _result("order_status", 0.9, entities, "lookup_order")

    if _contains_any(normalized, ["return", "refund", "exchange"]):
        return _result("return_policy", 0.86, entities, "search_policy")

    if _contains_any(normalized, ["shipping", "delivery", "ship", "arrive"]):
        return _result("shipping_policy", 0.82, entities, "search_policy")

    if _contains_any(normalized, ["warranty", "defect", "manufacturer", "water damage"]):
        return _result("warranty_policy", 0.82, entities, "search_policy")

    if _contains_any(normalized, ["recommend", "suggest", "looking for", "need a", "cheap", "budget"]):
        return _result("product_recommendation", 0.84, entities, "search_products")

    return _result("general_question", 0.55, entities, "answer_generally")


def _result(
    intent: Intent,
    confidence: float,
    entities: ExtractedEntities,
    suggested_action: str,
) -> IntentResult:
    return IntentResult(
        intent=intent,
        confidence=confidence,
        entities=entities,
        suggested_action=suggested_action,
    )


def _extract_order_id(message: str) -> int | None:
    match = ORDER_ID_PATTERN.search(message)
    if match is None:
        return None
    return int(match.group(1))


def _extract_budget(message: str) -> float | None:
    match = BUDGET_PATTERN.search(message)
    if match is None:
        return None
    return float(match.group(1))


def _extract_category(normalized_message: str) -> str | None:
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in normalized_message:
            return category
    return None


def _extract_keyword(normalized_message: str) -> str | None:
    category = _extract_category(normalized_message)
    if category:
        return category
    return None


def _contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)
