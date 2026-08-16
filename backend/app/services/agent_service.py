from app.schemas.chat import ChatRequest, ChatResponse, IntentResult
from app.schemas.order import Order
from app.schemas.product import Product
from app.services.intent_classifier import classify_message
from app.services.mock_data import get_order_by_id, search_products
from app.services.policy_search import search_policy


def handle_chat(request: ChatRequest) -> ChatResponse:
    intent_result = classify_message(request.message)

    if intent_result.intent == "order_status":
        return _handle_order_status(intent_result)

    if intent_result.intent == "product_recommendation":
        return _handle_product_recommendation(intent_result)

    if intent_result.intent in ["complaint", "human_escalation"]:
        return ChatResponse(
            answer="I am sorry this has been frustrating. I can create a support ticket for a human agent in the next step.",
            intent_result=intent_result,
            tool_used="create_support_ticket",
            tool_result={
                "status": "not_implemented",
                "reason": "Ticket creation will be added in a later step.",
            },
        )

    if intent_result.intent == "unsafe_private_request":
        return ChatResponse(
            answer="I cannot help with requests for another customer's private information.",
            intent_result=intent_result,
            tool_used="refuse_request",
            tool_result={"refused": True},
        )

    if intent_result.intent in ["return_policy", "shipping_policy", "warranty_policy"]:
        policy_type = intent_result.intent.replace("_policy", "")
        policy_chunks = search_policy(request.message, policy_type=policy_type)
        if policy_chunks:
            return ChatResponse(
                answer=_format_policy_answer(policy_chunks),
                intent_result=intent_result,
                tool_used="search_policy",
                tool_result=policy_chunks,
            )

        return ChatResponse(
            answer="I could not find a matching policy section for that question.",
            intent_result=intent_result,
            tool_used="search_policy",
            tool_result=[],
        )

    return ChatResponse(
        answer="I can help with customer support questions. Please share an order, product, policy, or issue.",
        intent_result=intent_result,
    )


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
