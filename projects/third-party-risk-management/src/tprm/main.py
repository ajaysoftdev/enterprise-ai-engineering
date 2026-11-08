"""FastAPI service for synthetic vendor risk and due-diligence workflow."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import VendorCreate, VendorRecord, EvidenceCreate, VendorDecision
from .risk import assess, missing_controls

app = FastAPI(
    title="Third-Party Risk Management",
    version="0.1.0",
    description="Synthetic vendor risk tiering, evidence tracking and approval gating.",
)


def assessment(vendor: dict) -> dict:
    evidence = repository.list_evidence(vendor["id"])
    missing = missing_controls(vendor["required_controls"], evidence)
    return {"vendor": vendor, "risk_factors": vendor["risk_factors"],
            "required_controls": vendor["required_controls"],
            "evidence": evidence, "missing_controls": missing,
            "evidence_complete": not missing}


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
    return {"status": "ok", "service": "third-party-risk-management"}


@app.post("/v1/vendors", response_model=VendorRecord, status_code=201)
def create_vendor(payload: VendorCreate):
    data = payload.model_dump()
    risk = assess(data)
    item = {
        "id": str(uuid4()), **data, **risk,
        "status": "DUE_DILIGENCE_REQUIRED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    repository.save_vendor(item)
    return item


@app.get("/v1/vendors/{vendor_id}", response_model=VendorRecord)
def get_vendor(vendor_id: str):
    item = repository.get_vendor(vendor_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return item


@app.post("/v1/vendors/{vendor_id}/evidence", response_model=dict, status_code=201)
def add_evidence(vendor_id: str, payload: EvidenceCreate):
    vendor = repository.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if payload.control_id not in vendor["required_controls"]:
        raise HTTPException(status_code=409, detail="Control is not required for this vendor risk tier")
    evidence = {"id": str(uuid4()), "vendor_id": vendor_id, **payload.model_dump(mode="json"),
                "created_at": datetime.now(timezone.utc).isoformat()}
    repository.save_evidence(evidence)
    return evidence


@app.get("/v1/vendors/{vendor_id}/assessment")
def get_assessment(vendor_id: str):
    vendor = repository.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return assessment(vendor)


@app.post("/v1/vendors/{vendor_id}/decision", response_model=VendorRecord)
def decide_vendor(vendor_id: str, payload: VendorDecision):
    vendor = repository.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if vendor["status"] != "DUE_DILIGENCE_REQUIRED":
        raise HTTPException(status_code=409, detail="Vendor decision already recorded")
    current = assessment(vendor)
    if payload.decision == "APPROVE" and current["missing_controls"]:
        raise HTTPException(status_code=409, detail="Required due-diligence evidence is incomplete")
    vendor["status"] = "APPROVED" if payload.decision == "APPROVE" else "REJECTED"
    repository.update_vendor(vendor)
    repository.save_decision({
        "id": str(uuid4()), "vendor_id": vendor_id, "decision": payload.decision,
        "approver": payload.approver, "note": payload.note,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return vendor
