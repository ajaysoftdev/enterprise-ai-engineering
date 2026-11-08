"""Typed API contracts for defensive simulation."""
from typing import Literal
from pydantic import BaseModel, Field


class AttackPath(BaseModel):
    principal: str
    nodes: list[str]
    relationships: list[str]
    target: str
    risk: Literal["HIGH", "MEDIUM", "LOW"]


class PolicyRequest(BaseModel):
    principal: str = Field(min_length=2, max_length=100)
    resource: str = Field(min_length=2, max_length=100)
    action: Literal["read", "write", "admin"]


class PolicyDecision(BaseModel):
    decision: Literal["ALLOW", "DENY"]
    reason: str
    principal: str
    resource: str
    action: str


class ContainmentRequest(BaseModel):
    principal: str = Field(min_length=2, max_length=100)
    incident_id: str = Field(min_length=3, max_length=100)
    approved_by: str | None = Field(default=None, min_length=2, max_length=120)


class ContainmentPlan(BaseModel):
    incident_id: str
    principal: str
    status: Literal["AWAITING_APPROVAL", "APPROVED_DRY_RUN"]
    actions: list[str]
    execution_mode: Literal["SIMULATION_ONLY"]
    note: str
