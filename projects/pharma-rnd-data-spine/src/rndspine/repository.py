"""SQLite persistence for synthetic scientific records and lineage edges."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("RND_SPINE_DB", "./data/rnd-spine.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS research_records (
      id TEXT PRIMARY KEY, source_system TEXT NOT NULL, source_record_id TEXT NOT NULL,
      study_id TEXT NOT NULL, record_type TEXT NOT NULL, record_name TEXT NOT NULL,
      schema_version TEXT NOT NULL, parent_record_ids TEXT NOT NULL, payload TEXT NOT NULL,
      status TEXT NOT NULL, quality_issues TEXT NOT NULL, created_at TEXT NOT NULL,
      UNIQUE(source_system, source_record_id)
    );
    CREATE TABLE IF NOT EXISTS lineage_edges (
      parent_id TEXT NOT NULL, child_id TEXT NOT NULL, created_at TEXT NOT NULL,
      PRIMARY KEY(parent_id, child_id)
    );
    CREATE TABLE IF NOT EXISTS audit_events (
      id TEXT PRIMARY KEY, record_id TEXT NOT NULL, action TEXT NOT NULL,
      details TEXT NOT NULL, created_at TEXT NOT NULL
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


def save_record(item: dict) -> None:
    execute("INSERT INTO research_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        item["id"],item["source_system"],item["source_record_id"],item["study_id"],
        item["record_type"],item["record_name"],item["schema_version"],
        json.dumps(item["parent_record_ids"]),json.dumps(item["payload"]),
        item["status"],json.dumps(item["quality_issues"]),item["created_at"]
    ))
    for parent_id in item["parent_record_ids"]:
        execute("INSERT INTO lineage_edges VALUES (?,?,?)",
                (parent_id,item["id"],item["created_at"]))


def get_record(record_id: str) -> dict | None:
    items = fetch("SELECT * FROM research_records WHERE id=?", (record_id,))
    if not items:
        return None
    item = items[0]
    item["parent_record_ids"] = json.loads(item["parent_record_ids"])
    item["payload"] = json.loads(item["payload"])
    item["quality_issues"] = json.loads(item["quality_issues"])
    return item


def list_records() -> list[dict]:
    ids = fetch("SELECT id FROM research_records ORDER BY created_at")
    return [get_record(item["id"]) for item in ids]


def upstream(record_id: str) -> list[dict]:
    visited = set()
    pending = [record_id]
    result = []
    while pending:
        current = pending.pop()
        for edge in fetch("SELECT parent_id FROM lineage_edges WHERE child_id=?", (current,)):
            parent = edge["parent_id"]
            if parent not in visited:
                visited.add(parent)
                result.append(get_record(parent))
                pending.append(parent)
    return [item for item in result if item]


def audit(event: dict) -> None:
    execute("INSERT INTO audit_events VALUES (?,?,?,?,?)", (
        event["id"],event["record_id"],event["action"],event["details"],event["created_at"]
    ))


def list_audit(record_id: str) -> list[dict]:
    return fetch("SELECT * FROM audit_events WHERE record_id=? ORDER BY created_at", (record_id,))
