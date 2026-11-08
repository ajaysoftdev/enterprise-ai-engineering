"""FastAPI endpoints for defensive attack-path and containment simulation."""
from fastapi import FastAPI
from .graph import paths_from, policy_decision, PRINCIPALS
from .models import PolicyRequest, PolicyDecision, ContainmentRequest, ContainmentPlan

app = FastAPI(
    title="Breach-Resilient Enterprise",
    version="0.1.0",
    description="Synthetic compromised-identity attack-path analysis and dry-run containment.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "breach-resilient-enterprise"}


@app.get("/v1/principals")
def list_principals() -> list[str]:
    return sorted(PRINCIPALS)


@app.get("/v1/attack-paths/{principal}")
def attack_paths(principal: str) -> dict:
    paths = paths_from(principal)
    return {"principal": principal, "paths": paths, "reachable_sensitive_targets": sorted({p["target"] for p in paths})}


@app.post("/v1/policies/evaluate", response_model=PolicyDecision)
def evaluate_policy(payload: PolicyRequest) -> dict:
    return {
        **policy_decision(payload.principal, payload.resource, payload.action),
        "principal": payload.principal, "resource": payload.resource, "action": payload.action,
    }


@app.post("/v1/containment/plan", response_model=ContainmentPlan)
def containment_plan(payload: ContainmentRequest) -> dict:
    paths = paths_from(payload.principal)
    targets = sorted({path["target"] for path in paths})
    actions = [
        "Disable or suspend the compromised principal in the identity provider",
        "Revoke active sessions and refresh tokens",
        "Review and rotate credentials reachable from the principal",
        "Isolate affected workloads after owner and impact validation",
        "Preserve relevant audit and forensic evidence",
        "Validate recovery and restore least-privilege access",
    ]
    if targets:
        actions.insert(3, "Prioritise reachable sensitive resources: " + ", ".join(targets))
    approved = bool(payload.approved_by)
    return {
        "incident_id": payload.incident_id,
        "principal": payload.principal,
        "status": "APPROVED_DRY_RUN" if approved else "AWAITING_APPROVAL",
        "actions": actions,
        "execution_mode": "SIMULATION_ONLY",
        "note": "No identity, workload, credential or network control is changed by this endpoint.",
    }
