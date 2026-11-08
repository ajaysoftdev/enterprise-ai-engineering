"""Explainable synthetic signal scoring; not a truth or credibility classifier."""
def score_signal(data: dict) -> dict:
    factors = {
        "source_reliability": round(data["source_reliability"] * 20),
        "reach": data["reach"] * 4,
        "velocity": data["velocity"] * 4,
        "corroboration": data["corroboration"] * 4,
        "business_impact": data["business_impact"] * 4,
    }
    score = min(100, sum(factors.values()))
    priority = "P1" if score >= 80 else "P2" if score >= 60 else "P3"
    return {"risk_score": score, "priority": priority, "risk_factors": factors}


def aggregate_case(signals: list[dict]) -> dict:
    highest = max(item["risk_score"] for item in signals)
    correlation_bonus = min(15, max(0, len(signals) - 1) * 5)
    score = min(100, highest + correlation_bonus)
    return {
        "signal_count": len(signals),
        "risk_score": score,
        "priority": "P1" if score >= 80 else "P2" if score >= 60 else "P3",
        "source_count": len({item["source_id"] for item in signals}),
        "explanation": "Case score combines the highest signal score with a capped shared-case corroboration increment.",
    }
