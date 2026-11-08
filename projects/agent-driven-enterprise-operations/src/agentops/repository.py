"""SQLite persistence for workflow state and audit events."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("AGENTOPS_DB", "./data/agentops.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS workflows (
      id TEXT PRIMARY KEY, workflow_type TEXT NOT NULL, requested_action TEXT NOT NULL,
      requester TEXT NOT NULL, request_text TEXT NOT NULL, selected_tool TEXT NOT NULL,
      planned_steps TEXT NOT NULL, risk TEXT NOT NULL, status TEXT NOT NULL,
      policy_reason TEXT NOT NULL, created_at TEXT NOT NULL, decided_by TEXT, decision_note TEXT
    );
    CREATE TABLE IF NOT EXISTS audit_events (
      id TEXT PRIMARY KEY, workflow_id TEXT NOT NULL, event_type TEXT NOT NULL,
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


def save_workflow(item: dict) -> None:
    execute("INSERT INTO workflows VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        item["id"],item["workflow_type"],item["requested_action"],item["requester"],
        item["request_text"],item["selected_tool"],json.dumps(item["planned_steps"]),
        item["risk"],item["status"],item["policy_reason"],item["created_at"],
        item.get("decided_by"),item.get("decision_note")
    ))


def get_workflow(workflow_id: str) -> dict | None:
    items = fetch("SELECT * FROM workflows WHERE id=?", (workflow_id,))
    if not items:
        return None
    item = items[0]
    item["planned_steps"] = json.loads(item["planned_steps"])
    return item


def update_decision(workflow_id: str, status: str, approver: str, note: str) -> None:
    execute("UPDATE workflows SET status=?, decided_by=?, decision_note=? WHERE id=?",
            (status, approver, note, workflow_id))


def append_audit(event: dict) -> None:
    execute("INSERT INTO audit_events VALUES (?,?,?,?,?,?)", (
        event["id"],event["workflow_id"],event["event_type"],
        event["actor"],event["details"],event["created_at"]
    ))


def list_audit(workflow_id: str) -> list[dict]:
    return fetch("SELECT * FROM audit_events WHERE workflow_id=? ORDER BY created_at", (workflow_id,))
