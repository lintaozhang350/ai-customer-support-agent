import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

from app.schemas.order import Order
from app.schemas.product import Product


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "support.db"

ORDER_SEEDS = [
    {
        "id": 1001,
        "user_id": 1,
        "status": "shipped",
        "item_name": "Wireless Keyboard",
        "tracking_number": "TRK-1001",
        "estimated_delivery": "2026-08-20",
        "created_at": "2026-08-12T09:30:00",
    },
    {
        "id": 1002,
        "user_id": 1,
        "status": "processing",
        "item_name": "USB-C Hub",
        "tracking_number": None,
        "estimated_delivery": "2026-08-23",
        "created_at": "2026-08-14T13:10:00",
    },
    {
        "id": 1003,
        "user_id": 2,
        "status": "delivered",
        "item_name": "Noise Cancelling Headphones",
        "tracking_number": "TRK-1003",
        "estimated_delivery": "2026-08-15",
        "created_at": "2026-08-09T16:45:00",
    },
    {
        "id": 1004,
        "user_id": 3,
        "status": "returned",
        "item_name": "Bluetooth Mouse",
        "tracking_number": "TRK-1004",
        "estimated_delivery": None,
        "created_at": "2026-08-01T11:05:00",
    },
    {
        "id": 1005,
        "user_id": 2,
        "status": "shipped",
        "item_name": "Portable Monitor",
        "tracking_number": "TRK-1005",
        "estimated_delivery": "2026-08-19",
        "created_at": "2026-08-11T08:20:00",
    },
]

PRODUCT_SEEDS = [
    {
        "id": 1,
        "name": "Budget Wireless Mouse",
        "category": "mouse",
        "price": 24.99,
        "description": "A compact wireless mouse for everyday productivity.",
        "inventory_count": 34,
    },
    {
        "id": 2,
        "name": "Ergonomic Bluetooth Mouse",
        "category": "mouse",
        "price": 39.99,
        "description": "A comfortable Bluetooth mouse with adjustable DPI.",
        "inventory_count": 18,
    },
    {
        "id": 3,
        "name": "Mechanical Keyboard Lite",
        "category": "keyboard",
        "price": 49.99,
        "description": "A compact mechanical keyboard with tactile switches.",
        "inventory_count": 22,
    },
    {
        "id": 4,
        "name": "Quiet Office Keyboard",
        "category": "keyboard",
        "price": 29.99,
        "description": "A low-profile keyboard built for quiet typing.",
        "inventory_count": 41,
    },
    {
        "id": 5,
        "name": "USB-C Travel Hub",
        "category": "accessory",
        "price": 34.99,
        "description": "A small USB-C hub with HDMI, USB-A, and SD card support.",
        "inventory_count": 27,
    },
    {
        "id": 6,
        "name": "Noise Cancelling Headphones",
        "category": "headphones",
        "price": 89.99,
        "description": "Wireless headphones with active noise cancellation.",
        "inventory_count": 12,
    },
]


def get_order_by_id(order_id: int) -> Order | None:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT id, user_id, status, item_name, tracking_number, estimated_delivery, created_at
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_order(row)


def search_products(
    category: str | None = None,
    budget: float | None = None,
    keyword: str | None = None,
) -> list[Product]:
    query = """
        SELECT id, name, category, price, description, inventory_count
        FROM products
        WHERE 1 = 1
    """
    parameters: list[object] = []

    if category:
        query += " AND lower(category) = lower(?)"
        parameters.append(category)

    if budget is not None:
        query += " AND price <= ?"
        parameters.append(budget)

    if keyword:
        query += """
            AND (
                lower(name) LIKE lower(?)
                OR lower(description) LIKE lower(?)
                OR lower(category) LIKE lower(?)
            )
        """
        keyword_pattern = f"%{keyword}%"
        parameters.extend([keyword_pattern, keyword_pattern, keyword_pattern])

    query += " ORDER BY id ASC"

    with _connect() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [_row_to_product(row) for row in rows]


def _connect() -> sqlite3.Connection:
    database_path = _database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    _create_tables(connection)
    _seed_catalog_if_needed(connection)
    return connection


def _database_path() -> Path:
    configured_path = os.getenv("SUPPORT_DB_PATH")
    if configured_path:
        return Path(configured_path)

    return DEFAULT_DATABASE_PATH


def _create_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            item_name TEXT NOT NULL,
            tracking_number TEXT,
            estimated_delivery TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            inventory_count INTEGER NOT NULL
        )
        """
    )
    connection.commit()


def _seed_catalog_if_needed(connection: sqlite3.Connection) -> None:
    order_count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    product_count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    if order_count == 0:
        connection.executemany(
            """
            INSERT INTO orders (
                id,
                user_id,
                status,
                item_name,
                tracking_number,
                estimated_delivery,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    order["id"],
                    order["user_id"],
                    order["status"],
                    order["item_name"],
                    order["tracking_number"],
                    order["estimated_delivery"],
                    order["created_at"],
                )
                for order in ORDER_SEEDS
            ],
        )

    if product_count == 0:
        connection.executemany(
            """
            INSERT INTO products (
                id,
                name,
                category,
                price,
                description,
                inventory_count
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    product["id"],
                    product["name"],
                    product["category"],
                    product["price"],
                    product["description"],
                    product["inventory_count"],
                )
                for product in PRODUCT_SEEDS
            ],
        )

    connection.commit()


def _row_to_order(row: sqlite3.Row) -> Order:
    estimated_delivery = None
    if row["estimated_delivery"] is not None:
        estimated_delivery = date.fromisoformat(row["estimated_delivery"])

    return Order(
        id=row["id"],
        user_id=row["user_id"],
        status=row["status"],
        item_name=row["item_name"],
        tracking_number=row["tracking_number"],
        estimated_delivery=estimated_delivery,
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_product(row: sqlite3.Row) -> Product:
    return Product(
        id=row["id"],
        name=row["name"],
        category=row["category"],
        price=row["price"],
        description=row["description"],
        inventory_count=row["inventory_count"],
    )
