"""Typed synthetic migration batch contracts."""
from typing import Any, Literal
from pydantic import BaseModel, Field


class SourceRecord(BaseModel):
    record_type: Literal["BUSINESS_PARTNER", "MATERIAL_MASTER"]
    source_key: str = Field(min_length=2, max_length=120)
    payload: dict[str, Any]


class MigrationCreate(BaseModel):
    idempotency_key: str = Field(min_length=4, max_length=120)
    source_system: str = Field(min_length=2, max_length=80)
    mapping_version: str = Field(min_length=1, max_length=40)
    records: list[SourceRecord] = Field(min_length=1, max_length=10000)


class MigrationReport(BaseModel):
    id: str
    idempotency_key: str
    source_system: str
    mapping_version: str
    source_count: int
    loaded_count: int
    quarantined_count: int
    target_count: int
    count_reconciled: bool
    status: str
    loaded_records: list[dict[str, Any]]
    quarantine: list[dict[str, Any]]
    created_at: str
