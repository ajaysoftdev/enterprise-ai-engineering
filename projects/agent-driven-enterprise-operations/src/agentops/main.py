"""FastAPI service for bounded, auditable enterprise-agent workflows."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import WorkflowCreate, ApprovalDecision, WorkflowRecord
from .policy import plan_for

app = FastAPI(
    title="Agent-Driven Enterprise Operations",
    version="0.1.0",
    description="Allow-listed procurement workflow planning with policy gates and human approval.",
)


def audit(workflow_id: str, event_type: str, actor: str, details: str) -> None:
    repository.append_audit({
        "id": str(uuid4()), "workflow_id": workflow_id, "event_type": event_type,
        "actor": actor, "details": details, "created_at": datetime.now(timezone.utc).isoformat(),
    })


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
    return {"status": "ok", "service": "agent-driven-enterprise-operations"}


@app.post("/v1/workflows", response_model=WorkflowRecord, status_code=201)
def create_workflow(payload: WorkflowCreate) -> dict:
    policy = plan_for(payload.requested_action)
    item = {
        "id": str(uuid4()), **payload.model_dump(),
        "selected_tool": policy["tool"], "planned_steps": policy["steps"],
        "risk": policy["risk"], "status": policy["status"],
        "policy_reason": policy["reason"], "created_at": datetime.now(timezone.utc).isoformat(),
        "decided_by": None, "decision_note": None,
    }
    repository.save_workflow(item)
    audit(item["id"], "WORKFLOW_CREATED", payload.requester, f"Selected allow-listed tool: {item['selected_tool']}")
    return item


@app.get("/v1/workflows/{workflow_id}", response_model=WorkflowRecord)
def get_workflow(workflow_id: str):
    item = repository.get_workflow(workflow_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return item


@app.post("/v1/workflows/{workflow_id}/decision", response_model=WorkflowRecord)
def decide_workflow(workflow_id: str, payload: ApprovalDecision):
    item = repository.get_workflow(workflow_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if item["status"] != "AWAITING_APPROVAL":
        raise HTTPException(status_code=409, detail="Workflow is not awaiting approval")
    status = "APPROVED_DRY_RUN" if payload.decision == "APPROVE" else "REJECTED"
    repository.update_decision(workflow_id, status, payload.approver, payload.note)
    audit(workflow_id, f"WORKFLOW_{payload.decision}", payload.approver, payload.note)
    return repository.get_workflow(workflow_id)


@app.get("/v1/workflows/{workflow_id}/audit")
def workflow_audit(workflow_id: str):
    if repository.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return repository.list_audit(workflow_id)
