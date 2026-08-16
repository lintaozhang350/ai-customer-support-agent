from datetime import date, datetime

from app.schemas.order import Order
from app.schemas.product import Product


ORDERS: list[Order] = [
    Order(
        id=1001,
        user_id=1,
        status="shipped",
        item_name="Wireless Keyboard",
        tracking_number="TRK-1001",
        estimated_delivery=date(2026, 8, 20),
        created_at=datetime(2026, 8, 12, 9, 30),
    ),
    Order(
        id=1002,
        user_id=1,
        status="processing",
        item_name="USB-C Hub",
        tracking_number=None,
        estimated_delivery=date(2026, 8, 23),
        created_at=datetime(2026, 8, 14, 13, 10),
    ),
    Order(
        id=1003,
        user_id=2,
        status="delivered",
        item_name="Noise Cancelling Headphones",
        tracking_number="TRK-1003",
        estimated_delivery=date(2026, 8, 15),
        created_at=datetime(2026, 8, 9, 16, 45),
    ),
    Order(
        id=1004,
        user_id=3,
        status="returned",
        item_name="Bluetooth Mouse",
        tracking_number="TRK-1004",
        estimated_delivery=None,
        created_at=datetime(2026, 8, 1, 11, 5),
    ),
    Order(
        id=1005,
        user_id=2,
        status="shipped",
        item_name="Portable Monitor",
        tracking_number="TRK-1005",
        estimated_delivery=date(2026, 8, 19),
        created_at=datetime(2026, 8, 11, 8, 20),
    ),
]


PRODUCTS: list[Product] = [
    Product(
        id=1,
        name="Budget Wireless Mouse",
        category="mouse",
        price=24.99,
        description="A compact wireless mouse for everyday productivity.",
        inventory_count=34,
    ),
    Product(
        id=2,
        name="Ergonomic Bluetooth Mouse",
        category="mouse",
        price=39.99,
        description="A comfortable Bluetooth mouse with adjustable DPI.",
        inventory_count=18,
    ),
    Product(
        id=3,
        name="Mechanical Keyboard Lite",
        category="keyboard",
        price=49.99,
        description="A compact mechanical keyboard with tactile switches.",
        inventory_count=22,
    ),
    Product(
        id=4,
        name="Quiet Office Keyboard",
        category="keyboard",
        price=29.99,
        description="A low-profile keyboard built for quiet typing.",
        inventory_count=41,
    ),
    Product(
        id=5,
        name="USB-C Travel Hub",
        category="accessory",
        price=34.99,
        description="A small USB-C hub with HDMI, USB-A, and SD card support.",
        inventory_count=27,
    ),
    Product(
        id=6,
        name="Noise Cancelling Headphones",
        category="headphones",
        price=89.99,
        description="Wireless headphones with active noise cancellation.",
        inventory_count=12,
    ),
]


def get_order_by_id(order_id: int) -> Order | None:
    return next((order for order in ORDERS if order.id == order_id), None)


def search_products(
    category: str | None = None,
    budget: float | None = None,
    keyword: str | None = None,
) -> list[Product]:
    results = PRODUCTS

    if category:
        category_lower = category.lower()
        results = [
            product
            for product in results
            if product.category.lower() == category_lower
        ]

    if budget is not None:
        results = [product for product in results if product.price <= budget]

    if keyword:
        keyword_lower = keyword.lower()
        results = [
            product
            for product in results
            if keyword_lower in product.name.lower()
            or keyword_lower in product.description.lower()
            or keyword_lower in product.category.lower()
        ]

    return results
