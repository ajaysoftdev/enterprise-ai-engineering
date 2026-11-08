"""SQLite persistence adapter for the local demonstrator."""
import json
import os
import sqlite3
from pathlib import Path
from .models import DocumentRecord


def database_path() -> str:
    return os.getenv("DOCUMENT_INTELLIGENCE_DB", "./data/documents.db")


def connect() -> sqlite3.Connection:
    path = Path(database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            id TEXT PRIMARY KEY,
            resource_id TEXT NOT NULL,
            action TEXT NOT NULL,
            actor TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            content_type TEXT NOT NULL,
            status TEXT NOT NULL,
            extracted_fields TEXT NOT NULL,
            validation_errors TEXT NOT NULL,
            created_at TEXT NOT NULL,
            reviewed_by TEXT,
            review_note TEXT
        )
    """)
    db.commit()
    return db


def save(record: DocumentRecord) -> None:
    with connect() as db:
        db.execute("""
            INSERT INTO documents
            (id, filename, content_type, status, extracted_fields,
             validation_errors, created_at, reviewed_by, review_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.id, record.filename, record.content_type, record.status,
            json.dumps({k: v.model_dump() for k, v in record.extracted_fields.items()}),
            json.dumps(record.validation_errors), record.created_at.isoformat(),
            record.reviewed_by, record.review_note,
        ))


def get(document_id: str) -> DocumentRecord | None:
    with connect() as db:
        row = db.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
    if row is None:
        return None
    return DocumentRecord(
        id=row["id"], filename=row["filename"], content_type=row["content_type"],
        status=row["status"], extracted_fields=json.loads(row["extracted_fields"]),
        validation_errors=json.loads(row["validation_errors"]),
        created_at=row["created_at"], reviewed_by=row["reviewed_by"],
        review_note=row["review_note"],
    )


def list_all(limit: int = 100) -> list[DocumentRecord]:
    with connect() as db:
        rows = db.execute(
            "SELECT id FROM documents ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [record for row in rows if (record := get(row["id"])) is not None]


def update_review(record: DocumentRecord) -> None:
    with connect() as db:
        db.execute("""
            UPDATE documents SET status = ?, reviewed_by = ?, review_note = ?
            WHERE id = ?
        """, (record.status, record.reviewed_by, record.review_note, record.id))


def append_audit(event_id: str, resource_id: str, action: str, actor: str, details: str, created_at: str) -> None:
    """Append an application audit event; there is intentionally no update/delete API."""
    with connect() as db:
        db.execute(
            "INSERT INTO audit_events (id, resource_id, action, actor, details, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (event_id, resource_id, action, actor, details, created_at),
        )


def list_audit(resource_id: str) -> list[dict[str, str]]:
    with connect() as db:
        rows = db.execute(
            "SELECT id, resource_id, action, actor, details, created_at FROM audit_events WHERE resource_id = ? ORDER BY created_at ASC",
            (resource_id,),
        ).fetchall()
    return [dict(row) for row in rows]
