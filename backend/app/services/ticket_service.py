from datetime import datetime

from app.schemas.ticket import SupportTicket, SupportTicketCreate


SUPPORT_TICKETS: list[SupportTicket] = []
NEXT_TICKET_ID = 1


def create_support_ticket(ticket_data: SupportTicketCreate) -> SupportTicket:
    global NEXT_TICKET_ID

    ticket = SupportTicket(
        id=NEXT_TICKET_ID,
        user_id=ticket_data.user_id,
        order_id=ticket_data.order_id,
        issue_type=ticket_data.issue_type,
        summary=ticket_data.summary,
        status="open",
        created_at=datetime.now(),
    )
    SUPPORT_TICKETS.append(ticket)
    NEXT_TICKET_ID += 1
    return ticket


def list_support_tickets() -> list[SupportTicket]:
    return SUPPORT_TICKETS


def get_support_ticket(ticket_id: int) -> SupportTicket | None:
    return next((ticket for ticket in SUPPORT_TICKETS if ticket.id == ticket_id), None)
