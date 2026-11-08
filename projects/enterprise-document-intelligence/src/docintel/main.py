"""FastAPI application for the local document intelligence demonstrator."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query
from . import repository
from .extraction import extract_fields, validate_fields
from .models import DocumentCreate, DocumentRecord, DocumentSummary, ReviewRequest

app = FastAPI(
    title="Enterprise Document Intelligence",
    version="0.1.0",
    description="Synthetic text intake, deterministic extraction, validation and human review.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-document-intelligence"}


@app.post("/v1/documents", response_model=DocumentRecord, status_code=201)
def create_document(payload: DocumentCreate) -> DocumentRecord:
    fields = extract_fields(payload.text_content)
    errors = validate_fields(fields)
    record = DocumentRecord(
        id=str(uuid4()),
        filename=payload.filename,
        content_type=payload.content_type,
        status="NEEDS_REVIEW" if errors else "RECEIVED",
        extracted_fields=fields,
        validation_errors=errors,
        created_at=datetime.now(timezone.utc),
    )
    repository.save(record)
    repository.append_audit(
        event_id=str(uuid4()), resource_id=record.id, action="DOCUMENT_RECEIVED",
        actor="system", details="Document submitted to local text-only prototype",
        created_at=record.created_at.isoformat(),
    )
    return record


@app.get("/v1/documents", response_model=list[DocumentSummary])
def list_documents(limit: int = Query(default=50, ge=1, le=100)) -> list[DocumentSummary]:
    return [
        DocumentSummary(id=r.id, filename=r.filename, status=r.status, created_at=r.created_at)
        for r in repository.list_all(limit)
    ]


@app.get("/v1/documents/{document_id}", response_model=DocumentRecord)
def get_document(document_id: str) -> DocumentRecord:
    record = repository.get(document_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return record


@app.post("/v1/documents/{document_id}/review", response_model=DocumentRecord)
def review_document(document_id: str, payload: ReviewRequest) -> DocumentRecord:
    record = repository.get(document_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if record.status not in ("RECEIVED", "NEEDS_REVIEW"):
        raise HTTPException(status_code=409, detail="Document has already been reviewed")
    record.status = payload.decision
    record.reviewed_by = payload.reviewer
    record.review_note = payload.note
    repository.update_review(record)
    repository.append_audit(
        event_id=str(uuid4()), resource_id=record.id, action=f"REVIEW_{payload.decision}",
        actor=payload.reviewer, details=payload.note,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    return record


@app.get("/v1/documents/{document_id}/audit")
def get_document_audit(document_id: str) -> list[dict[str, str]]:
    if repository.get(document_id) is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return repository.list_audit(document_id)
