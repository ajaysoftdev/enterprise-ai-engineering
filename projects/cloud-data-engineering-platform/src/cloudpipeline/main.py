"""FastAPI service for synthetic raw-to-curated batch data processing."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import PipelineRunCreate, PipelineRun
from .transform import process_rows

app = FastAPI(
    title="Cloud Data Engineering Platform",
    version="0.1.0",
    description="Synthetic batch ingestion, quality quarantine and bronze/silver/gold transformations.",
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
    return {"status": "ok", "service": "cloud-data-engineering-platform"}


@app.post("/v1/pipelines/sales/run", response_model=dict, status_code=201)
def run_sales_pipeline(payload: PipelineRunCreate):
    existing = repository.get_by_key(payload.idempotency_key)
    if existing:
        return {"run": existing, "duplicate": True}
    result = process_rows(payload.rows)
    created = datetime.now(timezone.utc).isoformat()
    item = {
        "id": str(uuid4()), "idempotency_key": payload.idempotency_key,
        "source_name": payload.source_name, "status": "COMPLETED_WITH_QUARANTINE" if result["quarantine"] else "COMPLETED",
        "raw_count": len(payload.rows), "accepted_count": len(result["curated_rows"]),
        "quarantined_count": len(result["quarantine"]), **result, "created_at": created,
    }
    try:
        repository.save(item)
    except sqlite3.IntegrityError:
        existing = repository.get_by_key(payload.idempotency_key)
        if existing:
            return {"run": existing, "duplicate": True}
        raise HTTPException(status_code=409, detail="Pipeline idempotency conflict")
    return {"run": item, "duplicate": False}


@app.get("/v1/pipelines/{run_id}", response_model=PipelineRun)
def get_pipeline_run(run_id: str):
    item = repository.get(run_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    return item
