"""SQLite storage for reproducible evaluation reports."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("AI_WORKBENCH_DB", "./data/ai-workbench.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL)")
    db.commit()
    return db


def save(report: dict) -> None:
    with closing(connect()) as db, db:
        db.execute("INSERT INTO reports VALUES (?,?,?)",
                   (report["id"],json.dumps(report),report["created_at"]))


def get(report_id: str) -> dict | None:
    with closing(connect()) as db:
        row = db.execute("SELECT payload FROM reports WHERE id=?", (report_id,)).fetchone()
    return json.loads(row["payload"]) if row else None


def list_all() -> list[dict]:
    with closing(connect()) as db:
        rows = db.execute("SELECT payload FROM reports ORDER BY created_at DESC").fetchall()
    return [json.loads(row["payload"]) for row in rows]
