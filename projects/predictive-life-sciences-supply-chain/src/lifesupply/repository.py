"""SQLite persistence for synthetic supply-risk scenarios."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("LIFESUPPLY_DB", "./data/lifesupply.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS scenarios (
      id TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS scenario_audit (
      id TEXT PRIMARY KEY, scenario_id TEXT NOT NULL, action TEXT NOT NULL,
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


def save(item: dict) -> None:
    execute("INSERT INTO scenarios VALUES (?,?,?)",
            (item["id"], json.dumps(item), item["created_at"]))


def get(scenario_id: str) -> dict | None:
    items = fetch("SELECT payload FROM scenarios WHERE id=?", (scenario_id,))
    return json.loads(items[0]["payload"]) if items else None


def list_all() -> list[dict]:
    return [json.loads(item["payload"]) for item in fetch("SELECT payload FROM scenarios ORDER BY created_at DESC")]


def audit(event: dict) -> None:
    execute("INSERT INTO scenario_audit VALUES (?,?,?,?,?,?)", (
        event["id"],event["scenario_id"],event["action"],event["actor"],
        event["details"],event["created_at"]
    ))


def list_audit(scenario_id: str) -> list[dict]:
    return fetch("SELECT * FROM scenario_audit WHERE scenario_id=? ORDER BY created_at", (scenario_id,))
