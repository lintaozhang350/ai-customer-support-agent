from fastapi import APIRouter, HTTPException

from app.schemas.ticket import SupportTicket, SupportTicketCreate
from app.services.ticket_service import (
    create_support_ticket,
    get_support_ticket,
    list_support_tickets,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[SupportTicket])
def read_tickets() -> list[SupportTicket]:
    return list_support_tickets()


@router.post("", response_model=SupportTicket)
def create_ticket(ticket_data: SupportTicketCreate) -> SupportTicket:
    return create_support_ticket(ticket_data)


@router.get("/{ticket_id}", response_model=SupportTicket)
def read_ticket(ticket_id: int) -> SupportTicket:
    ticket = get_support_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket
