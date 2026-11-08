"""Deterministic purpose- and classification-aware policy rules."""
from .models import AccessRequest

SENSITIVE = {"PERSONAL", "FINANCIAL", "CONFIDENTIAL"}


def evaluate(dataset: dict, request: AccessRequest) -> dict:
    field_map = {field["name"]: field["classification"] for field in dataset["fields"]}
    unknown = [name for name in request.requested_fields if name not in field_map]
    if unknown:
        return {"decision": "DENY", "allowed_fields": [], "denied_fields": request.requested_fields,
                "masking_required": True, "reason": "Requested field is not registered in the dataset"}
    if request.purpose not in {dataset["purpose"], "analytics", "privacy-review"}:
        return {"decision": "DENY", "allowed_fields": [], "denied_fields": request.requested_fields,
                "masking_required": True, "reason": "Purpose is not permitted for this dataset"}
    allowed = []
    denied = []
    for name in request.requested_fields:
        classification = field_map[name]
        permitted = False
        if request.role == "privacy-officer" and request.purpose == "privacy-review":
            permitted = True
        elif request.role == "finance-operator" and request.purpose == dataset["purpose"]:
            permitted = classification in {"PUBLIC", "INTERNAL", "FINANCIAL"}
        elif request.role in {"data-analyst", "data-owner"}:
            permitted = request.mode == "MASKED" and request.purpose in {dataset["purpose"], "analytics"}
        if permitted:
            allowed.append(name)
        else:
            denied.append(name)
    decision = "ALLOW" if allowed and not denied else "DENY"
    return {
        "decision": decision, "allowed_fields": allowed, "denied_fields": denied,
        "masking_required": request.mode == "MASKED" or request.role in {"data-analyst", "data-owner"},
        "reason": "All requested fields satisfy policy" if decision == "ALLOW"
                  else "One or more requested fields violate role, purpose or classification policy",
    }


def mask_value(value: str, classification: str, field_name: str) -> str:
    if classification not in SENSITIVE:
        return value
    lowered = field_name.lower()
    if "email" in lowered and "@" in value:
        local, domain = value.split("@", 1)
        return (local[:1] + "***@" + domain) if local else "***@" + domain
    if any(token in lowered for token in ("phone", "mobile")):
        return "***" + value[-4:] if len(value) > 4 else "***"
    if any(token in lowered for token in ("account", "tax", "card", "iban")):
        return "*" * max(0, len(value) - 4) + value[-4:]
    return "***MASKED***"


def mask_record(record: dict[str, str], dataset: dict) -> dict[str, str]:
    field_map = {field["name"]: field["classification"] for field in dataset["fields"]}
    return {name: mask_value(value, field_map.get(name, "CONFIDENTIAL"), name)
            for name, value in record.items()}
