"""FastAPI service for synthetic enterprise architecture assessments."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from . import repository
from .models import AssessmentCreate, AssessmentReport
from .analyzer import analyse

app = FastAPI(
    title="Enterprise Architecture Assessment Toolkit",
    version="0.1.0",
    description="Capability maturity, dependency findings and prioritised roadmap analysis.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-architecture-assessment-toolkit"}


@app.post("/v1/assessments", response_model=AssessmentReport, status_code=201)
def create_assessment(payload: AssessmentCreate):
    names = [item.name for item in payload.capabilities]
    if len(names) != len(set(names)):
        raise HTTPException(status_code=422, detail="Capability names must be unique")
    results = analyse([item.model_dump() for item in payload.capabilities],
                      [item.model_dump() for item in payload.dependencies])
    report = {
        "id": str(uuid4()), "assessment_name": payload.assessment_name,
        **results,
        "assumptions": [
            "Maturity ratings are stakeholder inputs, not independently verified facts.",
            "Roadmap priority is based on maturity gap only; cost, risk and strategic value require review.",
            "Dependency findings are descriptive and do not prove an operational dependency.",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    repository.save(report)
    return report


@app.get("/v1/assessments", response_model=list[AssessmentReport])
def list_assessments():
    return repository.list_all()


@app.get("/v1/assessments/{assessment_id}", response_model=AssessmentReport)
def get_assessment(assessment_id: str):
    report = repository.get(assessment_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return report
