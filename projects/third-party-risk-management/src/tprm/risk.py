"""Explainable deterministic inherent vendor risk scoring."""
from datetime import date

CONTROL_SETS = {
    "HIGH": ["access-control", "incident-response", "encryption", "business-continuity"],
    "MEDIUM": ["access-control", "incident-response"],
    "LOW": ["access-control"],
}


def assess(data: dict) -> dict:
    factors = {
        "service_criticality": data["service_criticality"] * 6,
        "data_sensitivity": data["data_sensitivity"] * 6,
        "internet_facing": 15 if data["internet_facing"] else 0,
        "privileged_access": 15 if data["privileged_access"] else 0,
        "fourth_party_exposure": min(data["fourth_party_count"], 5) * 2,
    }
    score = min(100, sum(factors.values()))
    tier = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
    return {"inherent_score": score, "risk_tier": tier, "risk_factors": factors,
            "required_controls": CONTROL_SETS[tier]}


def missing_controls(required: list[str], evidence: list[dict]) -> list[str]:
    today = date.today().isoformat()
    valid = {item["control_id"] for item in evidence if item["valid_until"] >= today}
    return [control for control in required if control not in valid]
