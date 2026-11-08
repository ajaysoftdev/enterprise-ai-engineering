"""SQLite workflow, idempotency and audit persistence."""
import hashlib
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def database_path() -> str:
    return os.getenv("PORTFOLIO_INTEGRATION_DB", "./data/portfolio-integration.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS workflows (
      id TEXT PRIMARY KEY,
      idempotency_key TEXT NOT NULL UNIQUE,
      payload_hash TEXT NOT NULL,
      request_payload TEXT NOT NULL,
      correlation_id TEXT NOT NULL,
      source_system TEXT NOT NULL,
      source_key TEXT NOT NULL,
      filename TEXT NOT NULL,
      state TEXT NOT NULL,
      document_id TEXT,
      source_record_id TEXT,
      match_candidate_id TEXT,
      golden_record_id TEXT,
      outcome TEXT,
      error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS audit_events (
      id TEXT PRIMARY KEY,
      workflow_id TEXT NOT NULL,
      action TEXT NOT NULL,
      from_state TEXT,
      to_state TEXT,
      details TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    """)
    db.commit()
    return db


def canonical_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _as_dict(row):
    return dict(row) if row is not None else None


def create_or_get(item: dict) -> tuple[dict, bool]:
    with closing(connect()) as db:
        db.execute("BEGIN IMMEDIATE")
        existing = db.execute(
            "SELECT * FROM workflows WHERE idempotency_key=?", (item["idempotency_key"],)
        ).fetchone()
        if existing:
            existing = dict(existing)
            if existing["payload_hash"] != item["payload_hash"]:
                raise ValueError("Idempotency key already used with a different payload")
            db.commit()
            return existing, True
        db.execute(
            """INSERT INTO workflows (
              id,idempotency_key,payload_hash,request_payload,correlation_id,
              source_system,source_key,filename,state,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (item["id"],item["idempotency_key"],item["payload_hash"],
             json.dumps(item["request_payload"], sort_keys=True),item["correlation_id"],
             item["source_system"],item["source_key"],item["filename"],item["state"],
             item["created_at"],item["updated_at"]),
        )
        db.execute(
            """INSERT INTO audit_events
            (id,workflow_id,action,from_state,to_state,details,created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (item["audit_id"],item["id"],"WORKFLOW_CREATED",None,item["state"],
             "Idempotent supplier onboarding request accepted",item["created_at"]),
        )
        db.commit()
        return get_workflow(item["id"]), False


def get_workflow(workflow_id: str) -> dict | None:
    with closing(connect()) as db:
        return _as_dict(db.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,)).fetchone())


def transition(workflow_id: str, state: str, details: str, audit_id: str, stamp: str, **updates) -> dict | None:
    allowed = {
        "document_id", "source_record_id", "match_candidate_id",
        "golden_record_id", "outcome", "error",
    }
    if not set(updates).issubset(allowed):
        raise ValueError("Unsupported workflow update field")
    with closing(connect()) as db:
        db.execute("BEGIN IMMEDIATE")
        current = db.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,)).fetchone()
        if current is None:
            db.rollback()
            return None
        old_state = current["state"]
        db.execute(
            """UPDATE workflows SET
              state=?, updated_at=?,
              document_id=CASE WHEN ? THEN ? ELSE document_id END,
              source_record_id=CASE WHEN ? THEN ? ELSE source_record_id END,
              match_candidate_id=CASE WHEN ? THEN ? ELSE match_candidate_id END,
              golden_record_id=CASE WHEN ? THEN ? ELSE golden_record_id END,
              outcome=CASE WHEN ? THEN ? ELSE outcome END,
              error=CASE WHEN ? THEN ? ELSE error END
              WHERE id=?""",
            (
                state, stamp,
                int("document_id" in updates), updates.get("document_id"),
                int("source_record_id" in updates), updates.get("source_record_id"),
                int("match_candidate_id" in updates), updates.get("match_candidate_id"),
                int("golden_record_id" in updates), updates.get("golden_record_id"),
                int("outcome" in updates), updates.get("outcome"),
                int("error" in updates), updates.get("error"),
                workflow_id,
            ),
        )
        db.execute(
            """INSERT INTO audit_events
            (id,workflow_id,action,from_state,to_state,details,created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (audit_id,workflow_id,"STATE_TRANSITION",old_state,state,details,stamp),
        )
        db.commit()
    return get_workflow(workflow_id)


def list_audit(workflow_id: str) -> list[dict]:
    with closing(connect()) as db:
        return [dict(row) for row in db.execute(
            "SELECT * FROM audit_events WHERE workflow_id=? ORDER BY created_at,id", (workflow_id,)
        ).fetchall()]
