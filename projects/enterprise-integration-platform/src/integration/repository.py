"""SQLite persistence for messages, delivery attempts and consumer deduplication."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("INTEGRATION_DB", "./data/integration.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS messages (
      id TEXT PRIMARY KEY, idempotency_key TEXT NOT NULL UNIQUE, producer TEXT NOT NULL,
      event_type TEXT NOT NULL, schema_version TEXT NOT NULL, correlation_id TEXT NOT NULL,
      payload TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL,
      last_error TEXT, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS processed_events (
      event_id TEXT PRIMARY KEY, processed_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS delivery_audit (
      id TEXT PRIMARY KEY, message_id TEXT NOT NULL, action TEXT NOT NULL,
      detail TEXT NOT NULL, created_at TEXT NOT NULL
    );
    """)
    db.commit()
    return db


def execute(sql: str, params: tuple = ()) -> None:
    with closing(connect()) as db, db:
        db.execute(sql, params)


def fetch(sql: str, params: tuple = ()) -> list[dict]:
    with closing(connect()) as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]


def save_message(item: dict) -> None:
    execute("INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
        item["id"],item["idempotency_key"],item["producer"],item["event_type"],
        item["schema_version"],item["correlation_id"],json.dumps(item["payload"]),
        item["status"],item["attempts"],item["last_error"],item["created_at"]
    ))


def get_message(message_id: str) -> dict | None:
    items = fetch("SELECT * FROM messages WHERE id=?", (message_id,))
    if not items:
        return None
    item = items[0]
    item["payload"] = json.loads(item["payload"])
    return item


def get_by_key(key: str) -> dict | None:
    items = fetch("SELECT * FROM messages WHERE idempotency_key=?", (key,))
    if not items:
        return None
    item = items[0]
    item["payload"] = json.loads(item["payload"])
    return item


def update_delivery(message_id: str, status: str, attempts: int, error: str | None) -> None:
    execute("UPDATE messages SET status=?, attempts=?, last_error=? WHERE id=?",
            (status, attempts, error, message_id))


def mark_processed(message_id: str, timestamp: str) -> bool:
    try:
        execute("INSERT INTO processed_events VALUES (?,?)", (message_id, timestamp))
        return True
    except sqlite3.IntegrityError:
        return False


def is_processed(message_id: str) -> bool:
    return bool(fetch("SELECT event_id FROM processed_events WHERE event_id=?", (message_id,)))


def audit(message_id: str, action: str, detail: str, timestamp: str) -> None:
    import uuid
    execute("INSERT INTO delivery_audit VALUES (?,?,?,?,?)",
            (str(uuid.uuid4()),message_id,action,detail,timestamp))


def list_dead_letters() -> list[dict]:
    items = fetch("SELECT * FROM messages WHERE status='DEAD_LETTER' ORDER BY created_at")
    for item in items:
        item["payload"] = json.loads(item["payload"])
    return items


def list_audit(message_id: str) -> list[dict]:
    return fetch("SELECT * FROM delivery_audit WHERE message_id=? ORDER BY created_at", (message_id,))
