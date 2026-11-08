"""Typed API and domain contracts."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    filename: str = Field(min_length=1, max_length=255)
    content_type: Literal["text/plain"]
    text_content: str = Field(min_length=1, max_length=200_000)


class ExtractedField(BaseModel):
    value: str | None
    confidence: float = Field(ge=0, le=1)
    evidence: str | None = None


class DocumentRecord(BaseModel):
    id: str
    filename: str
    content_type: str
    status: Literal["RECEIVED", "NEEDS_REVIEW", "APPROVED", "REJECTED"]
    extracted_fields: dict[str, ExtractedField]
    validation_errors: list[str]
    created_at: datetime
    reviewed_by: str | None = None
    review_note: str | None = None


class ReviewRequest(BaseModel):
    decision: Literal["APPROVED", "REJECTED"]
    reviewer: str = Field(min_length=2, max_length=120)
    note: str = Field(default="", max_length=1000)


class DocumentSummary(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime
