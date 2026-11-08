"""API contracts for data classification and policy evaluation."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Classification = Literal["PUBLIC", "INTERNAL", "CONFIDENTIAL", "PERSONAL", "FINANCIAL"]


class FieldDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    classification: Classification


class DatasetCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=2, max_length=160)
    owner: str = Field(min_length=2, max_length=120)
    purpose: str = Field(min_length=2, max_length=120)
    fields: list[FieldDefinition] = Field(min_length=1, max_length=100)


class DatasetRecord(BaseModel):
    id: str
    name: str
    owner: str
    purpose: str
    fields: list[FieldDefinition]
    created_at: str


class AccessRequest(BaseModel):
    dataset_id: str
    actor: str = Field(min_length=2, max_length=120)
    role: Literal["data-analyst", "finance-operator", "data-owner", "privacy-officer"]
    purpose: str = Field(min_length=2, max_length=120)
    requested_fields: list[str] = Field(min_length=1, max_length=100)
    mode: Literal["RAW", "MASKED"] = "MASKED"


class AccessDecision(BaseModel):
    decision: Literal["ALLOW", "DENY"]
    allowed_fields: list[str]
    denied_fields: list[str]
    masking_required: bool
    reason: str


class MaskRequest(BaseModel):
    records: list[dict[str, str]] = Field(min_length=1, max_length=100)


class MaskResponse(BaseModel):
    dataset_id: str
    records: list[dict[str, str]]
    masking_profile: str
