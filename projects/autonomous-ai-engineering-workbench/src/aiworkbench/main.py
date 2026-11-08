"""FastAPI service for static, reproducible AI coding-agent patch evaluation."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import EvaluationCreate, EvaluationReport
from .tasks import TASKS
from .evaluator import evaluate

app = FastAPI(
    title="Autonomous AI Engineering Workbench",
    version="0.1.0",
    description="Static patch evaluation with acceptance and security checks; submitted code is never executed.",
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
    return {"status": "ok", "service": "autonomous-ai-engineering-workbench"}


@app.get("/v1/tasks")
def list_tasks():
    return [{"task_id": key, "version": value["version"], "description": value["description"]}
            for key, value in TASKS.items()]


@app.post("/v1/evaluations", response_model=EvaluationReport, status_code=201)
def create_evaluation(payload: EvaluationCreate):
    if payload.task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Benchmark task not found")
    findings = evaluate(payload.task_id, payload.patch_files)
    report = {
        "id": str(uuid4()), "task_id": payload.task_id,
        "agent_profile": payload.agent_profile, **findings,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    repository.save(report)
    return report


@app.get("/v1/evaluations/{report_id}", response_model=EvaluationReport)
def get_evaluation(report_id: str):
    report = repository.get(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Evaluation report not found")
    return report


@app.get("/v1/evaluations", response_model=list[EvaluationReport])
def list_evaluations():
    return repository.list_all()
