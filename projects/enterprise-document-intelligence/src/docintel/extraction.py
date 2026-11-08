"""Deterministic baseline extractor. Replace with OCR/model adapters behind this boundary."""
import re
from .models import ExtractedField


def _field(pattern: str, text: str) -> ExtractedField:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ExtractedField(value=None, confidence=0.0, evidence=None)
    value = match.group(1).strip()
    return ExtractedField(value=value, confidence=0.90, evidence=match.group(0).strip())


def extract_fields(text: str) -> dict[str, ExtractedField]:
    """Extract a small set of labelled fields from synthetic/plain-text examples."""
    return {
        "document_number": _field(r"(?:invoice|document|po)\s*(?:number|no\.?|#)\s*[:\-]?\s*([A-Z0-9\-/]+)", text),
        "document_date": _field(r"(?:date|invoice date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", text),
        "total_amount": _field(r"(?:total|amount due)\s*[:\-]?\s*([A-Z]{0,3}\s?\d[\d,]*(?:\.\d{2})?)", text),
        "supplier": _field(r"(?:supplier|vendor)\s*[:\-]?\s*([^\r\n]{2,100})", text),
        "supplier_tax_id": _field(r"(?:supplier\s+)?(?:tax\s+id|tax identifier|gstin|vat id)\s*[:\-]?\s*([A-Z0-9-]{4,40})", text),
    }


def validate_fields(fields: dict[str, ExtractedField]) -> list[str]:
    errors: list[str] = []
    for required in ("document_number", "total_amount"):
        if not fields[required].value:
            errors.append(f"Missing required field: {required}")
    return errors
