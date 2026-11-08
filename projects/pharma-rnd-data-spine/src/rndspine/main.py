"""FastAPI service for scientific metadata intake and provenance queries."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import ResearchRecordCreate, ResearchRecord
from .quality import validate

app = FastAPI(
    title="Pharma R&D Data Spine",
    version="0.1.0",
    description="Synthetic research record intake, metadata quality and upstream lineage.",
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    """Attach a bounded correlation ID and baseline response headers."""
    import re
    import secrets
    supplied = request.headers.get("X-Request-ID", "")
    request_id = supplied if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", supplied) else secrets.token_hex(16)
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "pharma-rnd-data-spine"}


@app.post("/v1/records", response_model=ResearchRecord, status_code=201)
def ingest_record(payload: ResearchRecordCreate):
    for parent_id in payload.parent_record_ids:
        if repository.get_record(parent_id) is None:
            raise HTTPException(status_code=409, detail=f"Parent record not found: {parent_id}")
    created = datetime.now(timezone.utc).isoformat()
    item = {
        "id": str(uuid4()), **payload.model_dump(),
        "quality_issues": [], "created_at": created,
    }
    item["quality_issues"] = validate(item)
    item["status"] = "QUARANTINED" if item["quality_issues"] else "ACCEPTED"
    try:
        repository.save_record(item)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Source system/record identifier already exists")
    repository.audit({
        "id": str(uuid4()), "record_id": item["id"],
        "action": "RECORD_QUARANTINED" if item["quality_issues"] else "RECORD_ACCEPTED",
        "details": "; ".join(item["quality_issues"]) or "Metadata checks passed",
        "created_at": created,
    })
    return item


@app.get("/v1/records", response_model=list[ResearchRecord])
def list_records():
    return repository.list_records()


@app.get("/v1/records/{record_id}", response_model=ResearchRecord)
def get_record(record_id: str):
    item = repository.get_record(record_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Research record not found")
    return item


@app.get("/v1/records/{record_id}/lineage")
def get_lineage(record_id: str):
    item = repository.get_record(record_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Research record not found")
    return {"record": item, "upstream_records": repository.upstream(record_id)}


@app.get("/v1/records/{record_id}/audit")
def record_audit(record_id: str):
    if repository.get_record(record_id) is None:
        raise HTTPException(status_code=404, detail="Research record not found")
    return repository.list_audit(record_id)
