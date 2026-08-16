from app.schemas.chat import ChatHistoryMessage, ChatRequest, ChatResponse, IntentResult
from app.schemas.order import Order
from app.schemas.product import Product
from app.schemas.ticket import SupportTicketCreate
from app.services.llm_answer_generator import generate_answer_with_llm
from app.services.intent_classifier import classify_message
from app.services.llm_classifier import classify_message_with_llm
from app.services.mock_data import get_order_by_id, search_products
from app.services.policy_search import search_policy
from app.services.ticket_service import create_support_ticket


def handle_chat(
    request: ChatRequest,
    conversation_history: list[ChatHistoryMessage] | None = None,
) -> ChatResponse:
    history = conversation_history or []
    intent_result = classify_message_with_llm(
        request.message,
        conversation_history=history,
    ) or classify_message(request.message)
    intent_result = _apply_conversation_context(
        request.message,
        intent_result,
        history,
    )

    if intent_result.intent == "order_status":
        response = _handle_order_status(intent_result)
        return _finalize_response(request.message, response, history)

    if intent_result.intent == "product_recommendation":
        response = _handle_product_recommendation(intent_result)
        return _finalize_response(request.message, response, history)

    if intent_result.intent in ["complaint", "human_escalation"]:
        response = _handle_escalation(request, intent_result)
        return _finalize_response(request.message, response, history)

    if intent_result.intent == "unsafe_private_request":
        response = ChatResponse(
            answer="I cannot help with requests for another customer's private information.",
            intent_result=intent_result,
            tool_used="refuse_request",
            tool_result={"refused": True},
        )
        return _finalize_response(request.message, response, history)

    if intent_result.intent in ["return_policy", "shipping_policy", "warranty_policy"]:
        policy_type = intent_result.intent.replace("_policy", "")
        policy_chunks = search_policy(request.message, policy_type=policy_type)
        if policy_chunks:
            response = ChatResponse(
                answer=_format_policy_answer(policy_chunks),
                intent_result=intent_result,
                tool_used="search_policy",
                tool_result=policy_chunks,
            )
            return _finalize_response(request.message, response, history)

        response = ChatResponse(
            answer="I could not find a matching policy section for that question.",
            intent_result=intent_result,
            tool_used="search_policy",
            tool_result=[],
        )
        return _finalize_response(request.message, response, history)

    response = ChatResponse(
        answer="I can help with customer support questions. Please share an order, product, policy, or issue.",
        intent_result=intent_result,
    )
    return _finalize_response(request.message, response, history)


def _handle_order_status(intent_result: IntentResult) -> ChatResponse:
    order_id = intent_result.entities.order_id
    if order_id is None:
        return ChatResponse(
            answer="I can help check your order status. Please provide your order number.",
            intent_result=intent_result,
            tool_used="get_order_status",
            tool_result=None,
        )

    order = get_order_by_id(order_id)
    if order is None:
        return ChatResponse(
            answer=f"I could not find order {order_id}. Please double-check the order number and try again.",
            intent_result=intent_result,
            tool_used="get_order_status",
            tool_result=None,
        )

    return ChatResponse(
        answer=_format_order_answer(order),
        intent_result=intent_result,
        tool_used="get_order_status",
        tool_result=order.model_dump(mode="json"),
    )


def _handle_product_recommendation(intent_result: IntentResult) -> ChatResponse:
    products = search_products(
        category=intent_result.entities.category,
        budget=intent_result.entities.budget,
        keyword=intent_result.entities.keyword,
    )

    if not products:
        return ChatResponse(
            answer="I could not find matching products for those preferences. Try a different category or budget.",
            intent_result=intent_result,
            tool_used="search_products",
            tool_result=[],
        )

    return ChatResponse(
        answer=_format_product_answer(products),
        intent_result=intent_result,
        tool_used="search_products",
        tool_result=[product.model_dump(mode="json") for product in products],
    )


def _handle_escalation(
    request: ChatRequest,
    intent_result: IntentResult,
) -> ChatResponse:
    ticket = create_support_ticket(
        SupportTicketCreate(
            user_id=request.user_id,
            order_id=intent_result.entities.order_id,
            issue_type=intent_result.intent,
            summary=request.message,
        )
    )

    return ChatResponse(
        answer=f"I am sorry this has been frustrating. I created support ticket #{ticket.id}, and a human agent can follow up from there.",
        intent_result=intent_result,
        tool_used="create_support_ticket",
        tool_result=ticket.model_dump(mode="json"),
    )


def _format_order_answer(order: Order) -> str:
    if order.status == "shipped" and order.estimated_delivery:
        return f"Your order {order.id} for {order.item_name} has shipped and is estimated to arrive on {order.estimated_delivery}."

    if order.status == "processing":
        return f"Your order {order.id} for {order.item_name} is still processing. The estimated delivery date is {order.estimated_delivery}."

    if order.status == "delivered":
        return f"Your order {order.id} for {order.item_name} has been delivered."

    if order.status == "returned":
        return f"Your order {order.id} for {order.item_name} has been marked as returned."

    return f"Your order {order.id} is currently {order.status}."


def _format_product_answer(products: list[Product]) -> str:
    top_products = products[:3]
    product_summary = "; ".join(
        f"{product.name} (${product.price:.2f})" for product in top_products
    )
    return f"I found {len(products)} matching product(s): {product_summary}."


def _format_policy_answer(policy_chunks: list[dict[str, str | float]]) -> str:
    top_chunk = policy_chunks[0]
    policy_name = str(top_chunk["policy"]).replace("_", " ")
    source = top_chunk["source"]
    text = top_chunk["text"]
    return f"Based on the {policy_name} ({source}), {text}"


def _apply_conversation_context(
    message: str,
    intent_result: IntentResult,
    conversation_history: list[ChatHistoryMessage],
) -> IntentResult:
    if not conversation_history:
        return intent_result

    normalized = message.lower()
    contextual_order_id = _find_recent_order_id(conversation_history)
    contextual_category = _find_recent_category(conversation_history)

    updated_intent = intent_result.model_copy(deep=True)

    if updated_intent.entities.order_id is None and contextual_order_id is not None:
        if updated_intent.intent in ["complaint", "human_escalation", "order_status"]:
            updated_intent.entities.order_id = contextual_order_id

        if updated_intent.intent in ["shipping_policy", "general_question"] and _looks_like_order_follow_up(normalized):
            updated_intent.intent = "order_status"
            updated_intent.confidence = max(updated_intent.confidence, 0.79)
            updated_intent.suggested_action = "lookup_order"
            updated_intent.entities.order_id = contextual_order_id

    if updated_intent.entities.category is None and contextual_category is not None:
        if updated_intent.intent == "product_recommendation":
            updated_intent.entities.category = contextual_category
            if updated_intent.entities.keyword is None:
                updated_intent.entities.keyword = contextual_category

    return updated_intent


def _find_recent_order_id(conversation_history: list[ChatHistoryMessage]) -> int | None:
    for history_message in reversed(conversation_history):
        if history_message.role != "customer":
            continue

        result = classify_message(history_message.text)
        if result.entities.order_id is not None:
            return result.entities.order_id

    return None


def _find_recent_category(conversation_history: list[ChatHistoryMessage]) -> str | None:
    for history_message in reversed(conversation_history):
        if history_message.role != "customer":
            continue

        result = classify_message(history_message.text)
        if result.entities.category is not None:
            return result.entities.category

    return None


def _looks_like_order_follow_up(normalized_message: str) -> bool:
    has_reference = any(
        phrase in normalized_message
        for phrase in ["it", "that", "this order", "that order", "my order", "the order"]
    )
    has_tracking_language = any(
        phrase in normalized_message
        for phrase in ["arrive", "delivery", "deliver", "track", "status", "where"]
    )

    return has_reference and has_tracking_language


def _finalize_response(
    user_message: str,
    response: ChatResponse,
    conversation_history: list[ChatHistoryMessage],
) -> ChatResponse:
    rewritten_answer = generate_answer_with_llm(
        user_message=user_message,
        default_answer=response.answer,
        intent_result=response.intent_result,
        tool_used=response.tool_used,
        tool_result=response.tool_result,
        conversation_history=conversation_history,
    )

    if not rewritten_answer:
        return response

    return response.model_copy(update={"answer": rewritten_answer})
