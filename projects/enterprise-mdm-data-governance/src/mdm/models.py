"""API and domain contracts for the synthetic MDM demonstrator."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class SourceRecordCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    source_system: str = Field(min_length=2, max_length=80)
    source_key: str = Field(min_length=1, max_length=120)
    legal_name: str = Field(min_length=2, max_length=200)
    tax_id: str = Field(min_length=4, max_length=40)
    email: str | None = Field(default=None, max_length=254)


class SourceRecord(BaseModel):
    id: str
    source_system: str
    source_key: str
    legal_name: str
    tax_id: str
    email: str | None
    created_at: datetime


class MatchCandidate(BaseModel):
    id: str
    incoming_record_id: str
    existing_record_id: str
    match_rule: str
    status: Literal["PENDING", "CONFIRMED", "REJECTED"]
    created_at: datetime


class StewardDecision(BaseModel):
    decision: Literal["CONFIRM_MATCH", "REJECT_MATCH"]
    steward: str = Field(min_length=2, max_length=120)
    note: str = Field(default="", max_length=1000)


class GoldenRecord(BaseModel):
    id: str
    canonical_name: str
    tax_id: str
    source_record_ids: list[str]
    status: Literal["ACTIVE"]
    created_at: datetime
