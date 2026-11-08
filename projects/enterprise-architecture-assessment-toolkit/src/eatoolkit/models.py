"""Typed assessment, capability and dependency contracts."""
from typing import Literal
from pydantic import BaseModel, Field


class CapabilityInput(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    current_maturity: int = Field(ge=1, le=5)
    target_maturity: int = Field(ge=1, le=5)
    evidence_references: list[str] = Field(default_factory=list, max_length=20)


class DependencyInput(BaseModel):
    source_capability: str
    target_capability: str
    relationship: Literal["DEPENDS_ON", "SUPPORTS", "DUPLICATES"]


class AssessmentCreate(BaseModel):
    assessment_name: str = Field(min_length=2, max_length=160)
    business_objectives: list[str] = Field(min_length=1, max_length=20)
    capabilities: list[CapabilityInput] = Field(min_length=1, max_length=100)
    dependencies: list[DependencyInput] = Field(default_factory=list, max_length=300)


class AssessmentReport(BaseModel):
    id: str
    assessment_name: str
    overall_current_maturity: float
    overall_target_maturity: float
    capability_gaps: list[dict]
    dependency_findings: list[dict]
    roadmap: list[dict]
    assumptions: list[str]
    created_at: str
