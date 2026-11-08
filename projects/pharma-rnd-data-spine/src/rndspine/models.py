"""Typed synthetic scientific record and lineage contracts."""
from typing import Any, Literal
from pydantic import BaseModel, Field


class ResearchRecordCreate(BaseModel):
    source_system: str = Field(min_length=2, max_length=80)
    source_record_id: str = Field(min_length=2, max_length=120)
    study_id: str = Field(min_length=2, max_length=120)
    record_type: Literal["EXPERIMENT", "SAMPLE", "METHOD", "ASSAY_RESULT"]
    record_name: str = Field(min_length=2, max_length=160)
    schema_version: Literal["1.0"]
    parent_record_ids: list[str] = Field(default_factory=list, max_length=20)
    payload: dict[str, Any]


class ResearchRecord(BaseModel):
    id: str
    source_system: str
    source_record_id: str
    study_id: str
    record_type: str
    record_name: str
    schema_version: str
    parent_record_ids: list[str]
    payload: dict[str, Any]
    status: Literal["ACCEPTED", "QUARANTINED"]
    quality_issues: list[str]
    created_at: str
