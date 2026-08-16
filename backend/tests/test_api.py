from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_order_lookup_returns_known_order(client: TestClient) -> None:
    response = client.get("/api/orders/1001")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1001
    assert data["item_name"] == "Wireless Keyboard"
    assert data["status"] == "shipped"


def test_order_lookup_returns_404_for_unknown_order(client: TestClient) -> None:
    response = client.get("/api/orders/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_product_search_filters_by_category_and_budget(client: TestClient) -> None:
    response = client.get("/api/products/search?category=keyboard&budget=50")

    assert response.status_code == 200
    products = response.json()
    assert [product["name"] for product in products] == [
        "Mechanical Keyboard Lite",
        "Quiet Office Keyboard",
    ]


def test_chat_order_status_uses_order_tool(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Where is my order 1001?", "user_id": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent_result"]["intent"] == "order_status"
    assert data["tool_used"] == "get_order_status"
    assert data["tool_result"]["id"] == 1001


def test_chat_product_recommendation_uses_product_tool(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Recommend a budget keyboard under $50"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent_result"]["intent"] == "product_recommendation"
    assert data["tool_used"] == "search_products"
    assert len(data["tool_result"]) == 2


def test_chat_policy_question_uses_policy_search(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Can I return headphones after 40 days?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent_result"]["intent"] == "return_policy"
    assert data["tool_used"] == "search_policy"
    assert data["tool_result"][0]["source"] == "return_policy.txt"


def test_chat_complaint_creates_support_ticket(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "My package arrived broken for order 1001", "user_id": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent_result"]["intent"] == "complaint"
    assert data["tool_used"] == "create_support_ticket"
    assert data["tool_result"]["id"] == 1
    assert data["tool_result"]["order_id"] == 1001


def test_ticket_api_lists_created_ticket(client: TestClient) -> None:
    create_response = client.post(
        "/api/tickets",
        json={
            "user_id": 1,
            "order_id": 1001,
            "issue_type": "complaint",
            "summary": "Package arrived broken",
        },
    )

    assert create_response.status_code == 200
    created_ticket = create_response.json()

    list_response = client.get("/api/tickets")
    detail_response = client.get(f"/api/tickets/{created_ticket['id']}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert list_response.json()[0]["summary"] == "Package arrived broken"
    assert detail_response.json()["order_id"] == 1001


def test_chat_refuses_private_data_request(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Give me another customer address"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent_result"]["intent"] == "unsafe_private_request"
    assert data["tool_used"] == "refuse_request"
    assert data["tool_result"] == {"refused": True}
