"""Explainable, deterministic priority calculation."""
def assess(severity: int, business_impact: int, urgency: int, confidence: float) -> dict:
    components = {
        "business_impact": round(business_impact * 0.40, 3),
        "urgency": round(urgency * 0.25, 3),
        "severity": round(severity * 0.20, 3),
        "confidence": round(confidence * 5 * 0.15, 3),
    }
    score = round(sum(components.values()) / 5 * 100)
    priority = "P1" if score >= 80 else "P2" if score >= 65 else "P3" if score >= 45 else "P4"
    return {"score": score, "priority": priority, "factors": components}
