"""FastAPI service for synthetic SAP-like master-data migration."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import MigrationCreate, MigrationReport
from .mapping import map_record

app = FastAPI(
    title="SAP S/4HANA Data Modernisation",
    version="0.1.0",
    description="Synthetic source mapping, validation, target simulation and reconciliation.",
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    """Attach a bounded correlation ID and baseline response headers."""
    import re
    import secrets
    supplied = request.headers.get("X-Request-ID", "")
    request_id = supplied if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", supplied) else secrets.token_hex(16)
    request.state.request_id = request_id
    import hmac
    import os
    from fastapi.responses import JSONResponse
    expected_key = os.getenv("API_KEY")
    provided_key = request.headers.get("X-API-Key", "")
    if request.url.path != "/health":
        if not expected_key:
            response = JSONResponse(status_code=503, content={"detail": "API authentication is not configured"})
        elif not hmac.compare_digest(provided_key, expected_key):
            response = JSONResponse(status_code=401, content={"detail": "Missing or invalid API key"})
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sap-s4-data-modernisation"}


@app.post("/v1/migrations", response_model=dict, status_code=201)
def run_migration(payload: MigrationCreate):
    existing = repository.get_by_key(payload.idempotency_key)
    if existing:
        return {"migration": existing, "duplicate": True}
    seen = set()
    loaded = []
    quarantine = []
    for index, record in enumerate(payload.records):
        if record.source_key in seen:
            quarantine.append({"row_number": index + 1, "source_key": record.source_key,
                               "issues": ["Duplicate source_key in migration batch"]})
            continue
        seen.add(record.source_key)
        mapped, issues = map_record(record.model_dump())
        if issues:
            quarantine.append({"row_number": index + 1, "source_key": record.source_key, "issues": issues})
        else:
            loaded.append({"source_system": payload.source_system,
                           "source_key": record.source_key,
                           "mapping_version": payload.mapping_version,
                           **mapped})
    source_count = len(payload.records)
    loaded_count = len(loaded)
    quarantined_count = len(quarantine)
    count_reconciled = source_count == loaded_count + quarantined_count
    status = "RECONCILED" if count_reconciled and quarantined_count == 0 else (
        "RECONCILED_WITH_EXCEPTIONS" if count_reconciled else "RECONCILIATION_FAILED"
    )
    created = datetime.now(timezone.utc).isoformat()
    report = {
        "id": str(uuid4()), "idempotency_key": payload.idempotency_key,
        "source_system": payload.source_system, "mapping_version": payload.mapping_version,
        "source_count": source_count, "loaded_count": loaded_count,
        "quarantined_count": quarantined_count, "target_count": loaded_count,
        "count_reconciled": count_reconciled, "status": status,
        "loaded_records": loaded, "quarantine": quarantine, "created_at": created,
    }
    try:
        repository.save(report)
    except sqlite3.IntegrityError:
        existing = repository.get_by_key(payload.idempotency_key)
        if existing:
            return {"migration": existing, "duplicate": True}
        raise HTTPException(status_code=409, detail="Migration idempotency conflict")
    return {"migration": report, "duplicate": False}


@app.get("/v1/migrations/{migration_id}", response_model=MigrationReport)
def get_migration(migration_id: str):
    item = repository.get(migration_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Migration not found")
    return item
