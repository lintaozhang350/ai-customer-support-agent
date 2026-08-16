import os
import sqlite3
from datetime import datetime
from pathlib import Path

from app.schemas.ticket import SupportTicket, SupportTicketCreate


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "support.db"


def create_support_ticket(ticket_data: SupportTicketCreate) -> SupportTicket:
    created_at = datetime.now()

    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO support_tickets (
                user_id,
                order_id,
                issue_type,
                summary,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_data.user_id,
                ticket_data.order_id,
                ticket_data.issue_type,
                ticket_data.summary,
                "open",
                created_at.isoformat(),
            ),
        )
        connection.commit()
        ticket_id = cursor.lastrowid

    ticket = get_support_ticket(ticket_id)
    if ticket is None:
        raise RuntimeError("Created support ticket could not be loaded")

    return ticket


def list_support_tickets() -> list[SupportTicket]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, user_id, order_id, issue_type, summary, status, created_at
            FROM support_tickets
            ORDER BY id
            """
        ).fetchall()

    return [_row_to_ticket(row) for row in rows]


def get_support_ticket(ticket_id: int) -> SupportTicket | None:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT id, user_id, order_id, issue_type, summary, status, created_at
            FROM support_tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_ticket(row)


def reset_support_tickets_for_tests() -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM support_tickets")
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'support_tickets'")
        connection.commit()


def _connect() -> sqlite3.Connection:
    database_path = _database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    _create_tables(connection)
    return connection


def _database_path() -> Path:
    configured_path = os.getenv("SUPPORT_DB_PATH")
    if configured_path:
        return Path(configured_path)

    return DEFAULT_DATABASE_PATH


def _create_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_id INTEGER,
            issue_type TEXT NOT NULL,
            summary TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.commit()


def _row_to_ticket(row: sqlite3.Row) -> SupportTicket:
    return SupportTicket(
        id=row["id"],
        user_id=row["user_id"],
        order_id=row["order_id"],
        issue_type=row["issue_type"],
        summary=row["summary"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )
