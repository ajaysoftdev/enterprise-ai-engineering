"""FastAPI API for business-impact signal triage."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import SignalCreate, SignalRecord, AcknowledgeRequest
from .scoring import assess

app = FastAPI(
    title="Enterprise Attention and Intelligence Hub",
    version="0.1.0",
    description="Synthetic operational signal correlation and explainable business-impact prioritisation.",
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
    return {"status": "ok", "service": "enterprise-attention-intelligence-hub"}


@app.post("/v1/signals", response_model=SignalRecord, status_code=201)
def ingest_signal(payload: SignalCreate) -> dict:
    impact = assess(payload.severity, payload.business_impact, payload.urgency, payload.confidence)
    item = {
        "id": str(uuid4()), **payload.model_dump(), **impact,
        "status": "OPEN", "created_at": datetime.now(timezone.utc).isoformat(),
        "acknowledged_by": None,
    }
    repository.save(item)
    return item


@app.get("/v1/signals", response_model=list[SignalRecord])
def list_signals():
    return repository.list_signals()


@app.get("/v1/signals/{signal_id}", response_model=SignalRecord)
def get_signal(signal_id: str):
    item = repository.get(signal_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    return item


@app.get("/v1/correlations/{correlation_key}")
def get_correlation(correlation_key: str):
    signals = repository.by_correlation(correlation_key)
    if not signals:
        raise HTTPException(status_code=404, detail="Correlation group not found")
    highest = max(signals, key=lambda item: item["score"])
    return {
        "correlation_key": correlation_key,
        "signal_count": len(signals),
        "service_names": sorted({item["service_name"] for item in signals}),
        "highest_priority": highest["priority"],
        "highest_score": highest["score"],
        "signal_ids": [item["id"] for item in signals],
        "explanation": "Priority uses weighted business impact, urgency, technical severity and confidence.",
    }


@app.post("/v1/signals/{signal_id}/acknowledge", response_model=SignalRecord)
def acknowledge_signal(signal_id: str, payload: AcknowledgeRequest):
    item = repository.get(signal_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    if item["status"] == "ACKNOWLEDGED":
        raise HTTPException(status_code=409, detail="Signal already acknowledged")
    repository.acknowledge(signal_id, payload.actor)
    return repository.get(signal_id)
