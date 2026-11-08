"""SQLite persistence for information-risk signals, reviews and audit."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("INFO_RESILIENCE_DB", "./data/info-resilience.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS signals (
      id TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS reviews (
      id TEXT PRIMARY KEY, case_key TEXT NOT NULL, reviewer TEXT NOT NULL,
      decision TEXT NOT NULL, rationale TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS audit_events (
      id TEXT PRIMARY KEY, case_key TEXT NOT NULL, event_type TEXT NOT NULL,
      actor TEXT NOT NULL, details TEXT NOT NULL, created_at TEXT NOT NULL
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


def save_signal(item: dict) -> None:
    execute("INSERT INTO signals VALUES (?,?,?)", (item["id"],json.dumps(item),item["created_at"]))


def get_signal(signal_id: str) -> dict | None:
    items = fetch("SELECT payload FROM signals WHERE id=?", (signal_id,))
    return json.loads(items[0]["payload"]) if items else None


def list_signals(case_key: str) -> list[dict]:
    return [json.loads(item["payload"]) for item in fetch(
        "SELECT payload FROM signals WHERE json_extract(payload,'$.case_key')=? ORDER BY created_at", (case_key,)
    )]


def save_review(item: dict) -> None:
    execute("INSERT INTO reviews VALUES (?,?,?,?,?,?)", (
        item["id"],item["case_key"],item["reviewer"],item["decision"],
        item["rationale"],item["created_at"]
    ))


def list_reviews(case_key: str) -> list[dict]:
    return fetch("SELECT * FROM reviews WHERE case_key=? ORDER BY created_at", (case_key,))


def audit(event: dict) -> None:
    execute("INSERT INTO audit_events VALUES (?,?,?,?,?,?)", (
        event["id"],event["case_key"],event["event_type"],
        event["actor"],event["details"],event["created_at"]
    ))


def list_audit(case_key: str) -> list[dict]:
    return fetch("SELECT * FROM audit_events WHERE case_key=? ORDER BY created_at", (case_key,))
