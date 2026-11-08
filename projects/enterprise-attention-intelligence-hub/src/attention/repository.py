"""SQLite persistence for synthetic operational signals."""
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("ATTENTION_DB", "./data/attention.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS signals (
      id TEXT PRIMARY KEY, service_name TEXT NOT NULL, correlation_key TEXT NOT NULL,
      source TEXT NOT NULL, description TEXT NOT NULL, severity INTEGER NOT NULL,
      business_impact INTEGER NOT NULL, urgency INTEGER NOT NULL, confidence REAL NOT NULL,
      owner TEXT NOT NULL, score INTEGER NOT NULL, priority TEXT NOT NULL,
      status TEXT NOT NULL, created_at TEXT NOT NULL, acknowledged_by TEXT
    )""")
    db.commit()
    return db


def execute(sql: str, params: tuple = ()) -> None:
    with closing(connect()) as db, db:
        db.execute(sql, params)


def fetch(sql: str, params: tuple = ()) -> list[dict]:
    with closing(connect()) as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]


def save(item: dict) -> None:
    execute("""INSERT INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", tuple(item[k] for k in (
        "id","service_name","correlation_key","source","description","severity",
        "business_impact","urgency","confidence","owner","score","priority",
        "status","created_at","acknowledged_by"
    )))


def get(signal_id: str) -> dict | None:
    items = fetch("SELECT * FROM signals WHERE id=?", (signal_id,))
    return items[0] if items else None


def list_signals() -> list[dict]:
    return fetch("SELECT * FROM signals ORDER BY score DESC, created_at ASC")


def by_correlation(key: str) -> list[dict]:
    return fetch("SELECT * FROM signals WHERE correlation_key=? ORDER BY created_at", (key,))


def acknowledge(signal_id: str, actor: str) -> None:
    execute("UPDATE signals SET status='ACKNOWLEDGED', acknowledged_by=? WHERE id=?", (actor, signal_id))
