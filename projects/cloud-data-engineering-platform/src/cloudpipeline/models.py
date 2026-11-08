"""Typed batch pipeline contracts."""
from typing import Any
from pydantic import BaseModel, Field


class PipelineRunCreate(BaseModel):
    idempotency_key: str = Field(min_length=4, max_length=120)
    source_name: str = Field(min_length=2, max_length=120)
    rows: list[dict[str, Any]] = Field(min_length=1, max_length=10000)


class PipelineRun(BaseModel):
    id: str
    idempotency_key: str
    source_name: str
    status: str
    raw_count: int
    accepted_count: int
    quarantined_count: int
    duplicate_count: int
    curated_rows: list[dict[str, Any]]
    gold_summary: list[dict[str, Any]]
    quarantine: list[dict[str, Any]]
    created_at: str
