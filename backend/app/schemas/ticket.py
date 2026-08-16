from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


TicketStatus = Literal["open", "pending", "resolved"]
IssueType = Literal["complaint", "human_escalation", "general"]


class SupportTicketCreate(BaseModel):
    user_id: int | None = None
    order_id: int | None = None
    issue_type: IssueType = "general"
    summary: str = Field(min_length=1)


class SupportTicket(BaseModel):
    id: int
    user_id: int | None = None
    order_id: int | None = None
    issue_type: IssueType
    summary: str
    status: TicketStatus
    created_at: datetime
