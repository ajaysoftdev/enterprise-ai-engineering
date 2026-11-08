"""Typed synthetic supply scenario contracts."""
from typing import Literal
from pydantic import BaseModel, Field


class ScenarioCreate(BaseModel):
    material: str = Field(min_length=2, max_length=120)
    lot_id: str = Field(min_length=2, max_length=80)
    site: str = Field(min_length=2, max_length=100)
    available_quantity: float = Field(ge=0)
    daily_demand: float = Field(gt=0)
    replenishment_lead_days: int = Field(ge=0, le=365)
    production_order_due_days: int = Field(ge=0, le=365)
    quality_status: Literal["RELEASED", "HOLD", "QUARANTINED"]
    planner_owner: str = Field(min_length=2, max_length=120)


class SupplyScenario(BaseModel):
    id: str
    material: str
    lot_id: str
    site: str
    available_quantity: float
    daily_demand: float
    replenishment_lead_days: int
    production_order_due_days: int
    quality_status: str
    planner_owner: str
    days_of_cover: float
    projected_quantity_at_replenishment: float
    shortage_before_replenishment: bool
    risk_score: int
    priority: Literal["P1", "P2", "P3"]
    risk_reasons: list[str]
    recommended_actions: list[str]
    created_at: str
