from fastapi import APIRouter, Query

from app.schemas.product import Product
from app.services.mock_data import search_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search", response_model=list[Product])
def search_product_catalog(
    category: str | None = None,
    budget: float | None = Query(default=None, ge=0),
    keyword: str | None = None,
) -> list[Product]:
    return search_products(category=category, budget=budget, keyword=keyword)
