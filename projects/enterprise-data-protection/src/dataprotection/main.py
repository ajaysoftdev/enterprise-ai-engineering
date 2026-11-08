"""FastAPI service for synthetic data classification, masking and access policy."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import DatasetCreate, DatasetRecord, AccessRequest, AccessDecision, MaskRequest, MaskResponse
from .policy import evaluate, mask_record

app = FastAPI(
    title="Enterprise Data Protection",
    version="0.1.0",
    description="Synthetic dataset classification, purpose-aware access evaluation and masking.",
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
    return {"status": "ok", "service": "enterprise-data-protection"}


@app.post("/v1/datasets", response_model=DatasetRecord, status_code=201)
def register_dataset(payload: DatasetCreate) -> dict:
    item = {"id": str(uuid4()), **payload.model_dump(),
            "fields": [field.model_dump() for field in payload.fields],
            "created_at": datetime.now(timezone.utc).isoformat()}
    try:
        repository.save_dataset(item)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Dataset identifier conflict")
    return item


@app.get("/v1/datasets", response_model=list[DatasetRecord])
def list_datasets():
    return repository.list_datasets()


@app.get("/v1/datasets/{dataset_id}", response_model=DatasetRecord)
def get_dataset(dataset_id: str):
    item = repository.get_dataset(dataset_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return item


@app.post("/v1/access/evaluate", response_model=AccessDecision)
def evaluate_access(payload: AccessRequest):
    dataset = repository.get_dataset(payload.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    result = evaluate(dataset, payload)
    repository.audit({
        "id": str(uuid4()), "dataset_id": payload.dataset_id, "actor": payload.actor,
        "role": payload.role, "purpose": payload.purpose, "decision": result["decision"],
        "requested_fields": payload.requested_fields,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return result


@app.post("/v1/datasets/{dataset_id}/mask", response_model=MaskResponse)
def mask_dataset_records(dataset_id: str, payload: MaskRequest):
    dataset = repository.get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"dataset_id": dataset_id,
            "records": [mask_record(record, dataset) for record in payload.records],
            "masking_profile": "CLASSIFICATION_BASED_DETERMINISTIC"}
    

@app.get("/v1/datasets/{dataset_id}/audit")
def dataset_audit(dataset_id: str):
    if repository.get_dataset(dataset_id) is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return repository.list_audit(dataset_id)
