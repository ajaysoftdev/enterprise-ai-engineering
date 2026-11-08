"""SQLite persistence for vendor records, evidence and decisions."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("TPRM_DB", "./data/tprm.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS vendors (
      id TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS evidence (
      id TEXT PRIMARY KEY, vendor_id TEXT NOT NULL, control_id TEXT NOT NULL,
      evidence_reference TEXT NOT NULL, valid_until TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS decisions (
      id TEXT PRIMARY KEY, vendor_id TEXT NOT NULL, decision TEXT NOT NULL,
      approver TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL
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


def save_vendor(item: dict) -> None:
    execute("INSERT INTO vendors VALUES (?,?,?)", (item["id"],json.dumps(item),item["created_at"]))


def get_vendor(vendor_id: str) -> dict | None:
    items = fetch("SELECT payload FROM vendors WHERE id=?", (vendor_id,))
    return json.loads(items[0]["payload"]) if items else None


def update_vendor(item: dict) -> None:
    execute("UPDATE vendors SET payload=? WHERE id=?", (json.dumps(item),item["id"]))


def save_evidence(item: dict) -> None:
    execute("INSERT INTO evidence VALUES (?,?,?,?,?,?)", (
        item["id"],item["vendor_id"],item["control_id"],item["evidence_reference"],
        item["valid_until"],item["created_at"]
    ))


def list_evidence(vendor_id: str) -> list[dict]:
    return fetch("SELECT * FROM evidence WHERE vendor_id=? ORDER BY created_at", (vendor_id,))


def save_decision(item: dict) -> None:
    execute("INSERT INTO decisions VALUES (?,?,?,?,?,?)", (
        item["id"],item["vendor_id"],item["decision"],item["approver"],item["note"],item["created_at"]
    ))
