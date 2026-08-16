import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import ticket_service


@pytest.fixture(autouse=True)
def reset_support_tickets() -> None:
    ticket_service.SUPPORT_TICKETS.clear()
    ticket_service.NEXT_TICKET_ID = 1


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
