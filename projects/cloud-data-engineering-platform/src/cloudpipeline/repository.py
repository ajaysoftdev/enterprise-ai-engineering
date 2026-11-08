"""SQLite persistence for batch pipeline run metadata and output snapshots."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("CLOUD_PIPELINE_DB", "./data/cloud-pipeline.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS pipeline_runs (
      id TEXT PRIMARY KEY, idempotency_key TEXT NOT NULL UNIQUE, payload TEXT NOT NULL,
      created_at TEXT NOT NULL
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
    execute("INSERT INTO pipeline_runs VALUES (?,?,?,?)",
            (item["id"],item["idempotency_key"],json.dumps(item),item["created_at"]))


def get(run_id: str) -> dict | None:
    items = fetch("SELECT payload FROM pipeline_runs WHERE id=?", (run_id,))
    return json.loads(items[0]["payload"]) if items else None


def get_by_key(key: str) -> dict | None:
    items = fetch("SELECT payload FROM pipeline_runs WHERE idempotency_key=?", (key,))
    return json.loads(items[0]["payload"]) if items else None
