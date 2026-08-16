import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from app.schemas.chat import ChatHistoryMessage, ChatResponse, ConversationSummary


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "support.db"


def save_chat_exchange(
    conversation_id: str,
    user_id: int | None,
    customer_message: str,
    agent_response: ChatResponse,
) -> None:
    created_at = datetime.now()

    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO chat_messages (
                conversation_id,
                user_id,
                role,
                text,
                metadata,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                conversation_id,
                user_id,
                "customer",
                customer_message,
                None,
                created_at.isoformat(),
            ),
        )
        connection.execute(
            """
            INSERT INTO chat_messages (
                conversation_id,
                user_id,
                role,
                text,
                metadata,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                conversation_id,
                user_id,
                "agent",
                agent_response.answer,
                agent_response.model_dump_json(),
                datetime.now().isoformat(),
            ),
        )
        connection.commit()


def list_chat_messages(conversation_id: str) -> list[ChatHistoryMessage]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, user_id, role, text, metadata, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,),
        ).fetchall()

    return [_row_to_message(row) for row in rows]


def list_conversations(limit: int = 10) -> list[ConversationSummary]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                conversation_stats.conversation_id,
                conversation_stats.user_id,
                COALESCE(
                    (
                        SELECT customer_message.text
                        FROM chat_messages AS customer_message
                        WHERE customer_message.conversation_id = conversation_stats.conversation_id
                          AND customer_message.role = 'customer'
                        ORDER BY customer_message.id DESC
                        LIMIT 1
                    ),
                    (
                        SELECT any_message.text
                        FROM chat_messages AS any_message
                        WHERE any_message.conversation_id = conversation_stats.conversation_id
                        ORDER BY any_message.id DESC
                        LIMIT 1
                    )
                ) AS preview,
                conversation_stats.message_count,
                conversation_stats.last_message_at
            FROM (
                SELECT
                    conversation_id,
                    MAX(user_id) AS user_id,
                    COUNT(*) AS message_count,
                    MAX(created_at) AS last_message_at
                FROM chat_messages
                GROUP BY conversation_id
            ) AS conversation_stats
            ORDER BY last_message_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [_row_to_summary(row) for row in rows]


def reset_chat_messages_for_tests() -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM chat_messages")
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'chat_messages'")
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
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            user_id INTEGER,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            metadata TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.commit()


def _row_to_message(row: sqlite3.Row) -> ChatHistoryMessage:
    metadata: dict[str, Any] | None = None
    if row["metadata"] is not None:
        metadata = json.loads(row["metadata"])

    return ChatHistoryMessage(
        id=row["id"],
        conversation_id=row["conversation_id"],
        user_id=row["user_id"],
        role=row["role"],
        text=row["text"],
        metadata=metadata,
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_summary(row: sqlite3.Row) -> ConversationSummary:
    preview = row["preview"] or "Conversation"

    return ConversationSummary(
        conversation_id=row["conversation_id"],
        user_id=row["user_id"],
        preview=str(preview),
        message_count=row["message_count"],
        last_message_at=datetime.fromisoformat(row["last_message_at"]),
    )
