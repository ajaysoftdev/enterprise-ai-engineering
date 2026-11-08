"""FastAPI service for idempotent event intake, retries and DLQ replay."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import MessageCreate, MessageRecord, ProcessRequest

MAX_ATTEMPTS = 3
app = FastAPI(
    title="Enterprise Integration Platform",
    version="0.1.0",
    description="Synthetic message delivery with idempotency, bounded retry and dead-letter replay.",
)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    return {"status": "ok", "service": "enterprise-integration-platform"}


@app.post("/v1/messages", response_model=dict, status_code=202)
def publish_message(payload: MessageCreate) -> dict:
    existing = repository.get_by_key(payload.idempotency_key)
    if existing:
        return {"message": existing, "duplicate": True}
    item = {
        "id": str(uuid4()), **payload.model_dump(), "status": "PENDING",
        "attempts": 0, "last_error": None, "created_at": stamp(),
    }
    try:
        repository.save_message(item)
    except sqlite3.IntegrityError:
        existing = repository.get_by_key(payload.idempotency_key)
        if existing:
            return {"message": existing, "duplicate": True}
        raise HTTPException(status_code=409, detail="Message idempotency conflict")
    repository.audit(item["id"], "MESSAGE_ACCEPTED", "Message persisted to local delivery queue", item["created_at"])
    return {"message": item, "duplicate": False}


@app.get("/v1/messages/{message_id}", response_model=MessageRecord)
def get_message(message_id: str):
    item = repository.get_message(message_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return item


@app.post("/v1/messages/{message_id}/process", response_model=MessageRecord)
def process_message(message_id: str, payload: ProcessRequest):
    item = repository.get_message(message_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Message not found")
    if item["status"] in {"DELIVERED", "DEAD_LETTER"}:
        raise HTTPException(status_code=409, detail="Message is not eligible for processing")
    if repository.is_processed(message_id):
        repository.update_delivery(message_id, "DELIVERED", item["attempts"], None)
        return repository.get_message(message_id)
    attempts = item["attempts"] + 1
    if payload.simulate_failure:
        status = "DEAD_LETTER" if attempts >= MAX_ATTEMPTS else "RETRYING"
        error = "Synthetic target failure"
        repository.update_delivery(message_id, status, attempts, error)
        repository.audit(message_id, "DELIVERY_FAILED", f"Attempt {attempts}: {error}", stamp())
    else:
        repository.mark_processed(message_id, stamp())
        repository.update_delivery(message_id, "DELIVERED", attempts, None)
        repository.audit(message_id, "DELIVERY_SUCCEEDED", f"Delivered on attempt {attempts}", stamp())
    return repository.get_message(message_id)


@app.get("/v1/dead-letters", response_model=list[MessageRecord])
def dead_letters():
    return repository.list_dead_letters()


@app.post("/v1/dead-letters/{message_id}/replay", response_model=MessageRecord)
def replay_dead_letter(message_id: str):
    item = repository.get_message(message_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Message not found")
    if item["status"] != "DEAD_LETTER":
        raise HTTPException(status_code=409, detail="Only dead-letter messages can be replayed")
    repository.update_delivery(message_id, "PENDING", 0, None)
    repository.audit(message_id, "REPLAY_REQUESTED", "Authorised local replay requested", stamp())
    return repository.get_message(message_id)


@app.get("/v1/messages/{message_id}/audit")
def message_audit(message_id: str):
    if repository.get_message(message_id) is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return repository.list_audit(message_id)
