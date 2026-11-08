"""Typed event envelope and delivery contracts."""
from typing import Any, Literal
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    idempotency_key: str = Field(min_length=4, max_length=120)
    producer: str = Field(min_length=2, max_length=120)
    event_type: Literal["OrderCreated", "InventoryReserved", "ShipmentDispatched"]
    schema_version: Literal["1.0"]
    correlation_id: str = Field(min_length=3, max_length=120)
    payload: dict[str, Any]


class ProcessRequest(BaseModel):
    simulate_failure: bool = False


class MessageRecord(BaseModel):
    id: str
    idempotency_key: str
    producer: str
    event_type: str
    schema_version: str
    correlation_id: str
    payload: dict[str, Any]
    status: Literal["PENDING", "RETRYING", "DELIVERED", "DEAD_LETTER"]
    attempts: int
    last_error: str | None = None
    created_at: str
