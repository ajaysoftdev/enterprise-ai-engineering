"""Typed workflow and human approval contracts."""
from typing import Literal
from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    workflow_type: Literal["PROCUREMENT"]
    requested_action: Literal["gather_supplier_info", "draft_purchase_order", "submit_purchase_order", "delete_supplier"]
    requester: str = Field(min_length=2, max_length=120)
    request_text: str = Field(min_length=5, max_length=2000)


class ApprovalDecision(BaseModel):
    decision: Literal["APPROVE", "REJECT"]
    approver: str = Field(min_length=2, max_length=120)
    note: str = Field(default="", max_length=1000)


class WorkflowRecord(BaseModel):
    id: str
    workflow_type: str
    requested_action: str
    requester: str
    request_text: str
    selected_tool: str
    planned_steps: list[str]
    risk: Literal["LOW", "MEDIUM", "HIGH", "PROHIBITED"]
    status: Literal["READY", "AWAITING_APPROVAL", "APPROVED_DRY_RUN", "REJECTED", "BLOCKED"]
    policy_reason: str
    created_at: str
    decided_by: str | None = None
    decision_note: str | None = None
