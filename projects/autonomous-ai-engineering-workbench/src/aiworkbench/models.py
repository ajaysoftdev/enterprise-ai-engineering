"""Typed task and patch-evaluation contracts."""
from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    task_id: str = Field(min_length=2, max_length=100)
    agent_profile: str = Field(min_length=2, max_length=120)
    patch_files: dict[str, str] = Field(min_length=1, max_length=100)


class EvaluationReport(BaseModel):
    id: str
    task_id: str
    agent_profile: str
    score: int
    acceptance_score: int
    security_score: int
    evidence_score: int
    acceptance_findings: list[str]
    security_findings: list[str]
    test_execution: str
    merge_eligible: bool
    created_at: str
