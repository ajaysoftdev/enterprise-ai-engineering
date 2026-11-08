"""Typed contracts for operational signals and impact assessments."""
from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    service_name: str = Field(min_length=2, max_length=120)
    correlation_key: str = Field(min_length=2, max_length=120)
    source: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=3, max_length=500)
    severity: int = Field(ge=1, le=5)
    business_impact: int = Field(ge=1, le=5)
    urgency: int = Field(ge=1, le=5)
    confidence: float = Field(ge=0, le=1)
    owner: str = Field(min_length=2, max_length=120)


class AcknowledgeRequest(BaseModel):
    actor: str = Field(min_length=2, max_length=120)


class SignalRecord(BaseModel):
    id: str
    service_name: str
    correlation_key: str
    source: str
    description: str
    severity: int
    business_impact: int
    urgency: int
    confidence: float
    owner: str
    score: int
    priority: str
    status: str
    created_at: str
    acknowledged_by: str | None = None
