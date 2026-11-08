from fastapi.testclient import TestClient
from lifesupply.main import app
from lifesupply import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "supply.db"))


def scenario(**overrides):
    payload = {
        "material": "Sterile Vial 10ml", "lot_id": "LOT-SYN-1001",
        "site": "Plant-A", "available_quantity": 1000,
        "daily_demand": 100, "replenishment_lead_days": 5,
        "production_order_due_days": 8, "quality_status": "RELEASED",
        "planner_owner": "supply-planning"
    }
    payload.update(overrides)
    return payload


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_quality_hold_is_highest_priority(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/scenarios", json=scenario(quality_status="HOLD"))
    assert response.status_code == 201
    assert response.json()["risk_score"] == 100
    assert response.json()["priority"] == "P1"
    assert any("do not release" in action for action in response.json()["recommended_actions"])


def test_shortage_before_replenishment_is_high_priority(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/scenarios", json=scenario(available_quantity=200, daily_demand=100, replenishment_lead_days=5))
    assert response.status_code == 201
    assert response.json()["shortage_before_replenishment"] is True
    assert response.json()["priority"] == "P1"


def test_safe_supply_position_has_lower_priority(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/scenarios", json=scenario(available_quantity=5000, daily_demand=100, replenishment_lead_days=5))
    assert response.status_code == 201
    assert response.json()["priority"] == "P3"
    assert response.json()["shortage_before_replenishment"] is False


def test_invalid_zero_daily_demand_is_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/scenarios", json=scenario(daily_demand=0))
    assert response.status_code == 422


def test_risk_assessment_is_audited(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/scenarios", json=scenario()).json()
    events = client.get(f"/v1/scenarios/{created['id']}/audit").json()
    assert len(events) == 1
    assert events[0]["action"] == "RISK_ASSESSED"


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32
