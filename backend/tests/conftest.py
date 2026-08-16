import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import conversation_service, ticket_service


@pytest.fixture(autouse=True)
def reset_support_tickets(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("SUPPORT_DB_PATH", str(tmp_path / "support-test.db"))
    conversation_service.reset_chat_messages_for_tests()
    ticket_service.reset_support_tickets_for_tests()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
