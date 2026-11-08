from fastapi.testclient import TestClient
from attention.main import app
from attention import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "attention.db"))


def sample_signal(**overrides):
    payload = {
        "service_name": "order-management", "correlation_key": "INC-ORD-77",
        "source": "synthetic-monitor", "description": "Checkout latency above threshold",
        "severity": 4, "business_impact": 5, "urgency": 4,
        "confidence": 0.9, "owner": "commerce-platform"
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


def test_high_business_impact_signal_gets_high_priority(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/signals", json=sample_signal())
    assert response.status_code == 201
    assert response.json()["priority"] == "P1"
    assert response.json()["score"] >= 80


def test_related_signals_are_correlated_and_explained(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/signals", json=sample_signal())
    client.post("/v1/signals", json=sample_signal(
        service_name="payment-gateway", source="synthetic-apm",
        description="Payment API errors elevated", severity=3, business_impact=4
    ))
    response = client.get("/v1/correlations/INC-ORD-77")
    assert response.status_code == 200
    assert response.json()["signal_count"] == 2
    assert set(response.json()["service_names"]) == {"order-management", "payment-gateway"}


def test_low_impact_signal_is_lower_priority(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/signals", json=sample_signal(
        severity=1, business_impact=1, urgency=1, confidence=0.2
    ))
    assert response.json()["priority"] == "P4"


def test_acknowledgement_is_recorded(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/signals", json=sample_signal()).json()
    response = client.post(f"/v1/signals/{created['id']}/acknowledge", json={"actor": "on-call@example.test"})
    assert response.status_code == 200
    assert response.json()["status"] == "ACKNOWLEDGED"
    assert response.json()["acknowledged_by"] == "on-call@example.test"


def test_duplicate_acknowledgement_returns_conflict(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/signals", json=sample_signal()).json()
    client.post(f"/v1/signals/{created['id']}/acknowledge", json={"actor": "on-call@example.test"})
    response = client.post(f"/v1/signals/{created['id']}/acknowledge", json={"actor": "another@example.test"})
    assert response.status_code == 409


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401
    wrong_key = TestClient(app, headers={"X-API-Key": "incorrect-test-key"})
    assert wrong_key.get("/openapi.json").status_code == 401


def test_api_fails_closed_when_server_key_is_unconfigured(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    response = TestClient(app).get("/openapi.json")
    assert response.status_code == 503
