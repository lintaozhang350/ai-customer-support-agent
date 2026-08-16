from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


OrderStatus = Literal["processing", "shipped", "delivered", "returned"]


class Order(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    item_name: str
    tracking_number: str | None = None
    estimated_delivery: date | None = None
    created_at: datetime
