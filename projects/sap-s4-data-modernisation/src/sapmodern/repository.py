"""SQLite persistence for synthetic migration reports."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("SAP_MODERN_DB", "./data/sap-modern.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS migrations (id TEXT PRIMARY KEY, idempotency_key TEXT NOT NULL UNIQUE, payload TEXT NOT NULL, created_at TEXT NOT NULL)")
    db.commit()
    return db


def save(item: dict) -> None:
    with closing(connect()) as db, db:
        db.execute("INSERT INTO migrations VALUES (?,?,?,?)",
                   (item["id"],item["idempotency_key"],json.dumps(item),item["created_at"]))


def get(migration_id: str) -> dict | None:
    with closing(connect()) as db:
        row = db.execute("SELECT payload FROM migrations WHERE id=?", (migration_id,)).fetchone()
    return json.loads(row["payload"]) if row else None


def get_by_key(key: str) -> dict | None:
    with closing(connect()) as db:
        row = db.execute("SELECT payload FROM migrations WHERE idempotency_key=?", (key,)).fetchone()
    return json.loads(row["payload"]) if row else None
