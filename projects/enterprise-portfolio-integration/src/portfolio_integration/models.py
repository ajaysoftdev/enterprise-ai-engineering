"""Typed contracts for the supplier onboarding integration workflow."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class SupplierOnboardingRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    source_system: str = Field(min_length=2, max_length=80)
    source_key: str = Field(min_length=1, max_length=120)
    filename: str = Field(min_length=1, max_length=255)
    text_content: str = Field(min_length=1, max_length=200_000)


class WorkflowRecord(BaseModel):
    id: str
    idempotency_key: str
    correlation_id: str
    source_system: str
    source_key: str
    filename: str
    state: Literal[
        "RECEIVED", "DOCUMENT_REVIEW_REQUIRED", "WAITING_FOR_STEWARD",
        "COMPLETED", "DOWNSTREAM_FAILED"
    ]
    document_id: str | None = None
    source_record_id: str | None = None
    match_candidate_id: str | None = None
    golden_record_id: str | None = None
    outcome: str | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime
