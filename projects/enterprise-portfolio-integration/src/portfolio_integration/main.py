"""Cross-project supplier onboarding orchestration API."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, Header, HTTPException, Request
from . import repository
from .adapters import AdapterError, DocumentIntelligenceAdapter, MdmAdapter
from .models import SupplierOnboardingRequest, WorkflowRecord

app = FastAPI(
    title="Enterprise Portfolio Integration",
    version="0.1.0",
    description="Synthetic supplier invoice orchestration across Document Intelligence and MDM.",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def public_workflow(item: dict) -> dict:
    fields = WorkflowRecord.model_fields.keys()
    return {key: item.get(key) for key in fields}


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


app.state.document_adapter = DocumentIntelligenceAdapter()
app.state.mdm_adapter = MdmAdapter()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-portfolio-integration"}


@app.post("/v1/supplier-onboarding", status_code=202)
def start_supplier_onboarding(
    payload: SupplierOnboardingRequest,
    request: Request,
    idempotency_key: str = Header(alias="Idempotency-Key", min_length=4, max_length=120),
):
    stamp = now()
    body = payload.model_dump()
    item = {
        "id": str(uuid4()), "audit_id": str(uuid4()),
        "idempotency_key": idempotency_key,
        "payload_hash": repository.canonical_hash(body),
        "request_payload": body,
        "correlation_id": request.state.request_id,
        "source_system": payload.source_system,
        "source_key": payload.source_key,
        "filename": payload.filename,
        "state": "RECEIVED", "created_at": stamp, "updated_at": stamp,
    }
    try:
        workflow, duplicate = repository.create_or_get(item)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if duplicate:
        return {"workflow": public_workflow(workflow), "duplicate": True}

    try:
        document = app.state.document_adapter.submit({
            "filename": payload.filename,
            "content_type": "text/plain",
            "text_content": payload.text_content,
        }, request_id=request.state.request_id)
        document_id = document.get("id")
        if not document_id:
            workflow = repository.transition(
                workflow["id"], "DOWNSTREAM_FAILED",
                "Document Intelligence response did not contain a document ID",
                str(uuid4()), now(), error="Missing downstream document ID",
            )
            return {"workflow": public_workflow(workflow), "duplicate": False}
        fields = document.get("extracted_fields") or {}
        supplier = (fields.get("supplier") or {}).get("value")
        tax_id = (fields.get("supplier_tax_id") or {}).get("value")
        validation_errors = list(document.get("validation_errors") or [])
        if document.get("status") != "RECEIVED" or validation_errors or not supplier or not tax_id:
            reasons = validation_errors[:]
            if not supplier:
                reasons.append("Missing supplier identity")
            if not tax_id:
                reasons.append("Missing supplier tax identifier")
            workflow = repository.transition(
                workflow["id"], "DOCUMENT_REVIEW_REQUIRED",
                "; ".join(reasons) or "Document requires human review",
                str(uuid4()), now(), document_id=document_id,
                error="; ".join(reasons) or "Document requires human review",
            )
            return {"workflow": public_workflow(workflow), "duplicate": False}

        mdm_result = app.state.mdm_adapter.create_supplier({
            "source_system": payload.source_system,
            "source_key": payload.source_key,
            "legal_name": supplier,
            "tax_id": tax_id,
        }, request_id=request.state.request_id)
        source_record = mdm_result.get("source_record") or {}
        source_record_id = source_record.get("id")
        candidate = mdm_result.get("match_candidate")
        golden = mdm_result.get("golden_record")
        if candidate and candidate.get("id") and source_record_id:
            workflow = repository.transition(
                workflow["id"], "WAITING_FOR_STEWARD",
                "MDM returned a possible match; human stewardship is required",
                str(uuid4()), now(), document_id=document_id,
                source_record_id=source_record_id,
                match_candidate_id=candidate["id"],
            )
        elif golden and golden.get("id") and source_record_id:
            workflow = repository.transition(
                workflow["id"], "COMPLETED",
                "Document validated and MDM created a golden record",
                str(uuid4()), now(), document_id=document_id,
                source_record_id=source_record_id,
                golden_record_id=golden["id"], outcome="NEW_GOLDEN_RECORD",
            )
        else:
            workflow = repository.transition(
                workflow["id"], "DOWNSTREAM_FAILED",
                "MDM response did not include a source record and a candidate or golden record",
                str(uuid4()), now(), document_id=document_id,
                source_record_id=source_record_id,
                error="Unexpected MDM response",
            )
    except AdapterError as exc:
        workflow = repository.transition(
            workflow["id"], "DOWNSTREAM_FAILED", str(exc)[:500],
            str(uuid4()), now(), error=str(exc)[:500],
        )
    return {"workflow": public_workflow(workflow), "duplicate": False}


@app.get("/v1/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    workflow = repository.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return public_workflow(workflow)


@app.post("/v1/workflows/{workflow_id}/refresh")
def refresh_stewardship(workflow_id: str, request: Request):
    workflow = repository.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow["state"] != "WAITING_FOR_STEWARD":
        raise HTTPException(status_code=409, detail="Workflow is not waiting for MDM stewardship")
    try:
        result = app.state.mdm_adapter.refresh(
            workflow["match_candidate_id"], workflow["source_record_id"],
            request_id=request.state.request_id,
        )
    except AdapterError as exc:
        updated = repository.transition(
            workflow_id, "DOWNSTREAM_FAILED", str(exc)[:500],
            str(uuid4()), now(), error=str(exc)[:500],
        )
        return public_workflow(updated)
    status = result.get("candidate_status")
    if status == "PENDING":
        return public_workflow(workflow)
    if status not in {"CONFIRMED", "REJECTED"} or not result.get("golden_record_id"):
        updated = repository.transition(
            workflow_id, "DOWNSTREAM_FAILED", "MDM returned an unexpected stewardship outcome",
            str(uuid4()), now(), error="Unexpected MDM stewardship response",
        )
        return public_workflow(updated)
    outcome = "MATCH_CONFIRMED" if status == "CONFIRMED" else "SEPARATE_GOLDEN_RECORD"
    updated = repository.transition(
        workflow_id, "COMPLETED", f"MDM stewardship outcome: {status}",
        str(uuid4()), now(), golden_record_id=result["golden_record_id"], outcome=outcome,
    )
    return public_workflow(updated)


@app.get("/v1/workflows/{workflow_id}/audit")
def workflow_audit(workflow_id: str):
    if repository.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return repository.list_audit(workflow_id)
