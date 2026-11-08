"""FastAPI service for synthetic life-sciences supply risk analysis."""
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Request
from fastapi import FastAPI, HTTPException
from . import repository
from .models import ScenarioCreate, SupplyScenario
from .risk import assess

app = FastAPI(
    title="Predictive Life Sciences Supply Chain",
    version="0.1.0",
    description="Synthetic lot availability, quality hold and replenishment risk assessment.",
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    """Attach a bounded correlation ID and baseline response headers."""
    import re
    import secrets
    supplied = request.headers.get("X-Request-ID", "")
    request_id = supplied if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", supplied) else secrets.token_hex(16)
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "predictive-life-sciences-supply-chain"}


@app.post("/v1/scenarios", response_model=SupplyScenario, status_code=201)
def create_scenario(payload: ScenarioCreate):
    created = datetime.now(timezone.utc).isoformat()
    item = {
        "id": str(uuid4()), **payload.model_dump(),
        **assess(payload.model_dump()), "created_at": created,
    }
    repository.save(item)
    repository.audit({
        "id": str(uuid4()), "scenario_id": item["id"], "action": "RISK_ASSESSED",
        "actor": "system", "details": f"Risk score {item['risk_score']} / {item['priority']}",
        "created_at": created,
    })
    return item


@app.get("/v1/scenarios", response_model=list[SupplyScenario])
def list_scenarios():
    return repository.list_all()


@app.get("/v1/scenarios/{scenario_id}", response_model=SupplyScenario)
def get_scenario(scenario_id: str):
    item = repository.get(scenario_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return item


@app.get("/v1/scenarios/{scenario_id}/audit")
def scenario_audit(scenario_id: str):
    if repository.get(scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return repository.list_audit(scenario_id)
