"""FastAPI service for synthetic master-data ingestion and stewardship."""
from datetime import datetime, timezone
from uuid import uuid4
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from . import repository
from .models import SourceRecordCreate, SourceRecord, MatchCandidate, StewardDecision, GoldenRecord

app = FastAPI(
    title="Enterprise MDM and Data Governance",
    version="0.1.0",
    description="Synthetic supplier source-record matching and human stewardship demonstrator.",
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def normalise_tax_id(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum())


def create_golden(source: dict) -> dict:
    golden = {
        "id": str(uuid4()), "canonical_name": source["legal_name"],
        "tax_id": normalise_tax_id(source["tax_id"]),
        "source_record_ids": [source["id"]], "status": "ACTIVE",
        "created_at": source["created_at"],
    }
    repository.save_golden(golden)
    return golden


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-mdm-data-governance"}


@app.post("/v1/source-records", response_model=dict, status_code=201)
def ingest_source_record(payload: SourceRecordCreate) -> dict:
    stamp = now()
    record = {
        "id": str(uuid4()), **payload.model_dump(),
        "tax_id": payload.tax_id.strip(), "created_at": stamp.isoformat(),
    }
    try:
        repository.save_source(record)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Source system/key already exists")
    existing = repository.rows("SELECT * FROM source_records WHERE id<>? ORDER BY created_at", (record["id"],))
    match = next((item for item in existing
                  if normalise_tax_id(item["tax_id"]) == normalise_tax_id(record["tax_id"])), None)
    if match:
        candidate = {
            "id": str(uuid4()), "incoming_record_id": record["id"],
            "existing_record_id": match["id"], "match_rule": "EXACT_NORMALISED_TAX_ID",
            "status": "PENDING", "created_at": stamp.isoformat(),
        }
        repository.save_candidate(candidate)
        return {"source_record": record, "match_candidate": candidate, "golden_record": None}
    golden = create_golden(record)
    return {"source_record": record, "match_candidate": None, "golden_record": golden}


@app.get("/v1/match-candidates", response_model=list[MatchCandidate])
def list_match_candidates(status: str | None = Query(default=None, pattern="^(PENDING|CONFIRMED|REJECTED)$")):
    return repository.list_candidates(status)


@app.post("/v1/match-candidates/{candidate_id}/decision", response_model=dict)
def decide_match(candidate_id: str, payload: StewardDecision) -> dict:
    try:
        return repository.apply_steward_decision(
            candidate_id, payload.model_dump(), str(uuid4()), now().isoformat()
        )
    except LookupError as exc:
        raise HTTPException(status_code=404 if str(exc) == "Match candidate not found" else 409,
                            detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/v1/golden-records", response_model=list[GoldenRecord])
def list_golden_records():
    import json
    return [
        {**item, "source_record_ids": json.loads(item["source_record_ids"])}
        for item in repository.list_golden()
    ]
