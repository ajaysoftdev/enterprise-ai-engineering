"""FastAPI service for static, reproducible AI coding-agent patch evaluation."""
from datetime import datetime, timezone
from uuid import uuid4
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
