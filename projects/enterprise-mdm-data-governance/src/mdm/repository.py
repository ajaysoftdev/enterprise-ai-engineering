"""SQLite repository for the local synthetic-data MDM prototype."""
import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from uuid import uuid4


def database_path() -> str:
    return os.getenv("MDM_DATABASE", "./data/mdm.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS source_records (
      id TEXT PRIMARY KEY, source_system TEXT NOT NULL, source_key TEXT NOT NULL,
      legal_name TEXT NOT NULL, tax_id TEXT NOT NULL, email TEXT, created_at TEXT NOT NULL,
      UNIQUE(source_system, source_key)
    );
    CREATE TABLE IF NOT EXISTS match_candidates (
      id TEXT PRIMARY KEY, incoming_record_id TEXT NOT NULL, existing_record_id TEXT NOT NULL,
      match_rule TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS golden_records (
      id TEXT PRIMARY KEY, canonical_name TEXT NOT NULL, tax_id TEXT NOT NULL,
      source_record_ids TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS steward_decisions (
      id TEXT PRIMARY KEY, candidate_id TEXT NOT NULL, decision TEXT NOT NULL,
      steward TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL
    );
    """)
    db.commit()
    return db


def rows(sql: str, params: tuple = ()) -> list[dict]:
    with closing(connect()) as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]


def row(sql: str, params: tuple = ()) -> dict | None:
    found = rows(sql, params)
    return found[0] if found else None


def execute(sql: str, params: tuple = ()) -> None:
    with closing(connect()) as db, db:
        db.execute(sql, params)


def save_source(record: dict) -> None:
    execute("""INSERT INTO source_records
      (id,source_system,source_key,legal_name,tax_id,email,created_at)
      VALUES (?,?,?,?,?,?,?)""",
      (record["id"],record["source_system"],record["source_key"],record["legal_name"],
       record["tax_id"],record.get("email"),record["created_at"]))


def save_candidate(candidate: dict) -> None:
    execute("""INSERT INTO match_candidates
      (id,incoming_record_id,existing_record_id,match_rule,status,created_at)
      VALUES (?,?,?,?,?,?)""",
      (candidate["id"],candidate["incoming_record_id"],candidate["existing_record_id"],
       candidate["match_rule"],candidate["status"],candidate["created_at"]))


def save_golden(golden: dict) -> None:
    execute("""INSERT INTO golden_records
      (id,canonical_name,tax_id,source_record_ids,status,created_at)
      VALUES (?,?,?,?,?,?)""",
      (golden["id"],golden["canonical_name"],golden["tax_id"],
       json.dumps(golden["source_record_ids"]),golden["status"],golden["created_at"]))


def add_source_to_golden(golden_id: str, source_id: str) -> None:
    current = row("SELECT source_record_ids FROM golden_records WHERE id=?", (golden_id,))
    if current is None:
        raise LookupError("Golden record not found")
    ids = json.loads(current["source_record_ids"])
    if source_id not in ids:
        ids.append(source_id)
        execute("UPDATE golden_records SET source_record_ids=? WHERE id=?", (json.dumps(ids),golden_id))


def save_decision(decision: dict) -> None:
    execute("""INSERT INTO steward_decisions
      (id,candidate_id,decision,steward,note,created_at) VALUES (?,?,?,?,?,?)""",
      (decision["id"],decision["candidate_id"],decision["decision"],
       decision["steward"],decision["note"],decision["created_at"]))


def update_candidate(candidate_id: str, status: str) -> None:
    execute("UPDATE match_candidates SET status=? WHERE id=?", (status,candidate_id))


def get_source(record_id: str) -> dict | None:
    return row("SELECT * FROM source_records WHERE id=?", (record_id,))


def get_candidate(candidate_id: str) -> dict | None:
    return row("SELECT * FROM match_candidates WHERE id=?", (candidate_id,))


def list_candidates(status: str | None = None) -> list[dict]:
    if status:
        return rows("SELECT * FROM match_candidates WHERE status=? ORDER BY created_at", (status,))
    return rows("SELECT * FROM match_candidates ORDER BY created_at")


def list_golden() -> list[dict]:
    return rows("SELECT * FROM golden_records ORDER BY created_at")


def golden_for_source(source_id: str) -> dict | None:
    import json
    for item in list_golden():
        if source_id in json.loads(item["source_record_ids"]):
            return item
    return None


def apply_steward_decision(candidate_id: str, payload: dict, decision_id: str, stamp: str) -> dict:
    """Apply candidate state, steward decision and golden-record change atomically."""
    with closing(connect()) as db:
        db.execute("BEGIN IMMEDIATE")
        candidate_row = db.execute(
            "SELECT * FROM match_candidates WHERE id=?", (candidate_id,)
        ).fetchone()
        if candidate_row is None:
            raise LookupError("Match candidate not found")
        candidate = dict(candidate_row)
        if candidate["status"] != "PENDING":
            raise ValueError("Match candidate has already been decided")
        incoming_row = db.execute(
            "SELECT * FROM source_records WHERE id=?", (candidate["incoming_record_id"],)
        ).fetchone()
        if incoming_row is None:
            raise LookupError("Incoming source record is unavailable")
        incoming = dict(incoming_row)
        status = "CONFIRMED" if payload["decision"] == "CONFIRM_MATCH" else "REJECTED"
        updated = db.execute(
            "UPDATE match_candidates SET status=? WHERE id=? AND status='PENDING'",
            (status, candidate_id),
        )
        if updated.rowcount != 1:
            raise ValueError("Match candidate has already been decided")
        decision = {
            "id": decision_id, "candidate_id": candidate_id,
            "decision": payload["decision"], "steward": payload["steward"],
            "note": payload["note"], "created_at": stamp,
        }
        db.execute(
            """INSERT INTO steward_decisions
            (id,candidate_id,decision,steward,note,created_at) VALUES (?,?,?,?,?,?)""",
            (decision["id"], decision["candidate_id"], decision["decision"],
             decision["steward"], decision["note"], decision["created_at"]),
        )
        if status == "CONFIRMED":
            golden_rows = db.execute("SELECT * FROM golden_records ORDER BY created_at").fetchall()
            golden = next(
                (dict(item) for item in golden_rows
                 if candidate["existing_record_id"] in json.loads(item["source_record_ids"])),
                None,
            )
            if golden is None:
                raise LookupError("Existing source has no golden record")
            ids = json.loads(golden["source_record_ids"])
            if incoming["id"] not in ids:
                ids.append(incoming["id"])
                db.execute(
                    "UPDATE golden_records SET source_record_ids=? WHERE id=?",
                    (json.dumps(ids), golden["id"]),
                )
            golden["source_record_ids"] = json.dumps(ids)
        else:
            golden = {
                "id": str(uuid4()),
                "canonical_name": incoming["legal_name"],
                "tax_id": "".join(ch for ch in incoming["tax_id"].upper() if ch.isalnum()),
                "source_record_ids": json.dumps([incoming["id"]]),
                "status": "ACTIVE", "created_at": stamp,
            }
            db.execute(
                """INSERT INTO golden_records
                (id,canonical_name,tax_id,source_record_ids,status,created_at)
                VALUES (?,?,?,?,?,?)""",
                (golden["id"], golden["canonical_name"], golden["tax_id"],
                 golden["source_record_ids"], golden["status"], golden["created_at"]),
            )
        db.commit()
        candidate["status"] = status
        golden["source_record_ids"] = json.loads(golden["source_record_ids"])
        return {"candidate": candidate, "steward_decision": decision, "golden_record": golden}
