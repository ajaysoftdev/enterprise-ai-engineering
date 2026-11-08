"""Explainable deterministic supply-risk calculation; not a validated forecast model."""
def assess(data: dict) -> dict:
    cover = data["available_quantity"] / data["daily_demand"]
    projected = data["available_quantity"] - data["daily_demand"] * data["replenishment_lead_days"]
    shortage = projected < 0
    reasons = []
    actions = []
    score = 20
    if data["quality_status"] in {"HOLD", "QUARANTINED"}:
        score = 100
        reasons.append(f"Lot quality status is {data['quality_status']}")
        actions.append("Escalate to authorised Quality personnel; do not release or consume the lot")
    if shortage:
        score = max(score, 90)
        reasons.append("Projected demand exceeds available quantity before replenishment")
        actions.append("Planner to evaluate alternate released lots, transfers or rescheduling")
    if cover < 7:
        score = max(score, 75)
        reasons.append("Less than seven days of supply cover")
        actions.append("Planner to review near-term demand and replenishment options")
    if not reasons:
        reasons.append("No immediate quality hold or replenishment-window shortage detected")
        actions.append("Continue routine monitoring and reconcile the next supply event")
    priority = "P1" if score >= 90 else "P2" if score >= 70 else "P3"
    return {
        "days_of_cover": round(cover, 2),
        "projected_quantity_at_replenishment": round(projected, 2),
        "shortage_before_replenishment": shortage,
        "risk_score": score, "priority": priority,
        "risk_reasons": reasons, "recommended_actions": actions,
    }
