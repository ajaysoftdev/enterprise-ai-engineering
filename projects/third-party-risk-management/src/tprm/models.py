"""Typed vendor intake, evidence and approval contracts."""
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field


class VendorCreate(BaseModel):
    vendor_name: str = Field(min_length=2, max_length=160)
    service_name: str = Field(min_length=2, max_length=160)
    service_criticality: int = Field(ge=1, le=5)
    data_sensitivity: int = Field(ge=1, le=5)
    internet_facing: bool
    privileged_access: bool
    fourth_party_count: int = Field(ge=0, le=100)
    owner: str = Field(min_length=2, max_length=120)


class EvidenceCreate(BaseModel):
    control_id: Literal["access-control", "incident-response", "encryption", "business-continuity"]
    evidence_reference: str = Field(min_length=3, max_length=240)
    valid_until: date


class VendorDecision(BaseModel):
    decision: Literal["APPROVE", "REJECT"]
    approver: str = Field(min_length=2, max_length=120)
    note: str = Field(default="", max_length=1000)


class VendorRecord(BaseModel):
    id: str
    vendor_name: str
    service_name: str
    service_criticality: int
    data_sensitivity: int
    internet_facing: bool
    privileged_access: bool
    fourth_party_count: int
    owner: str
    inherent_score: int
    risk_tier: Literal["HIGH", "MEDIUM", "LOW"]
    status: Literal["DUE_DILIGENCE_REQUIRED", "APPROVED", "REJECTED"]
    created_at: str
