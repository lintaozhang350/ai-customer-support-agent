from fastapi import APIRouter, HTTPException

from app.schemas.order import Order
from app.services.mock_data import get_order_by_id

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int) -> Order:
    order = get_order_by_id(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
