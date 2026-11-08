"""SQLite metadata and policy-decision audit persistence."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("DATA_PROTECTION_DB", "./data/data-protection.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS datasets (
      id TEXT PRIMARY KEY, name TEXT NOT NULL, owner TEXT NOT NULL,
      purpose TEXT NOT NULL, fields TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS policy_audit (
      id TEXT PRIMARY KEY, dataset_id TEXT NOT NULL, actor TEXT NOT NULL,
      role TEXT NOT NULL, purpose TEXT NOT NULL, decision TEXT NOT NULL,
      requested_fields TEXT NOT NULL, created_at TEXT NOT NULL
    );
    """)
    db.commit()
    return db


def execute(sql: str, params: tuple = ()) -> None:
    with closing(connect()) as db, db:
        db.execute(sql, params)


def fetch(sql: str, params: tuple = ()) -> dict | None:
    with closing(connect()) as db:
        row = db.execute(sql, params).fetchone()
        return dict(row) if row else None


def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    with closing(connect()) as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]


def save_dataset(item: dict) -> None:
    execute("INSERT INTO datasets VALUES (?,?,?,?,?,?)", (
        item["id"], item["name"], item["owner"], item["purpose"],
        json.dumps(item["fields"]), item["created_at"]
    ))


def get_dataset(dataset_id: str) -> dict | None:
    item = fetch("SELECT * FROM datasets WHERE id=?", (dataset_id,))
    if item:
        item["fields"] = json.loads(item["fields"])
    return item


def list_datasets() -> list[dict]:
    items = fetch_all("SELECT * FROM datasets ORDER BY created_at")
    for item in items:
        item["fields"] = json.loads(item["fields"])
    return items


def audit(event: dict) -> None:
    execute("INSERT INTO policy_audit VALUES (?,?,?,?,?,?,?,?)", (
        event["id"], event["dataset_id"], event["actor"], event["role"],
        event["purpose"], event["decision"], json.dumps(event["requested_fields"]),
        event["created_at"]
    ))


def list_audit(dataset_id: str) -> list[dict]:
    return fetch_all("SELECT * FROM policy_audit WHERE dataset_id=? ORDER BY created_at", (dataset_id,))
