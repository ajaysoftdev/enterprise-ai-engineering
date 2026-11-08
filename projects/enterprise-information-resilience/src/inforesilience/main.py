"""FastAPI service for synthetic information-risk signals and human review."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from . import repository
from .models import SignalCreate, SignalRecord, ReviewDecision
from .scoring import score_signal, aggregate_case

app = FastAPI(
    title="Enterprise Information Resilience",
    version="0.1.0",
    description="Synthetic signal scoring, shared-case correlation and human review; no automated public response.",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit(case_key: str, event_type: str, actor: str, details: str):
    repository.audit({"id": str(uuid4()), "case_key": case_key, "event_type": event_type,
                      "actor": actor, "details": details, "created_at": now()})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-information-resilience"}


@app.post("/v1/signals", response_model=SignalRecord, status_code=201)
def ingest_signal(payload: SignalCreate):
    data = payload.model_dump()
    item = {"id": str(uuid4()), **data, **score_signal(data), "created_at": now()}
    repository.save_signal(item)
    audit(item["case_key"], "SIGNAL_INGESTED", item["source_id"], "Synthetic signal stored with evidence reference")
    return item


@app.get("/v1/cases/{case_key}")
def get_case(case_key: str):
    signals = repository.list_signals(case_key)
    if not signals:
        raise HTTPException(status_code=404, detail="Case not found")
    reviews = repository.list_reviews(case_key)
    latest_review = reviews[-1] if reviews else None
    return {
        "case_key": case_key, **aggregate_case(signals),
        "signals": signals, "reviews": reviews,
        "status": latest_review["decision"] if latest_review else "PENDING_REVIEW",
    }


@app.post("/v1/cases/{case_key}/review")
def review_case(case_key: str, payload: ReviewDecision):
    signals = repository.list_signals(case_key)
    if not signals:
        raise HTTPException(status_code=404, detail="Case not found")
    reviews = repository.list_reviews(case_key)
    if reviews:
        raise HTTPException(status_code=409, detail="Case already has a review decision")
    item = {
        "id": str(uuid4()), "case_key": case_key, "reviewer": payload.reviewer,
        "decision": payload.decision, "rationale": payload.rationale, "created_at": now(),
    }
    repository.save_review(item)
    audit(case_key, "HUMAN_REVIEW_RECORDED", payload.reviewer, payload.decision + ": " + payload.rationale)
    return {"case_key": case_key, "status": payload.decision, "review": item,
            "external_response_executed": False}


@app.get("/v1/cases/{case_key}/audit")
def case_audit(case_key: str):
    if not repository.list_signals(case_key):
        raise HTTPException(status_code=404, detail="Case not found")
    return repository.list_audit(case_key)
