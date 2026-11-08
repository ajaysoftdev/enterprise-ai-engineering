"""Typed synthetic information-risk and human-review contracts."""
from typing import Literal
from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    case_key: str = Field(min_length=3, max_length=120)
    source_id: str = Field(min_length=2, max_length=120)
    source_type: Literal["PUBLIC_WEB", "INTERNAL", "PARTNER"]
    evidence_reference: str = Field(min_length=3, max_length=500)
    claim_text: str = Field(min_length=5, max_length=2000)
    source_reliability: float = Field(ge=0, le=1)
    reach: int = Field(ge=0, le=5)
    velocity: int = Field(ge=0, le=5)
    corroboration: int = Field(ge=0, le=5)
    business_impact: int = Field(ge=0, le=5)


class ReviewDecision(BaseModel):
    reviewer: str = Field(min_length=2, max_length=120)
    decision: Literal["CONFIRM_RISK", "DISMISS", "NEEDS_EVIDENCE"]
    rationale: str = Field(min_length=3, max_length=1000)


class SignalRecord(BaseModel):
    id: str
    case_key: str
    source_id: str
    source_type: str
    evidence_reference: str
    claim_text: str
    source_reliability: float
    reach: int
    velocity: int
    corroboration: int
    business_impact: int
    risk_score: int
    priority: Literal["P1", "P2", "P3"]
    created_at: str
