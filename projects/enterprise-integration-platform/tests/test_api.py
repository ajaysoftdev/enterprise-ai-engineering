from fastapi.testclient import TestClient
from integration.main import app
from integration import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "integration.db"))


def sample_message(key="ORDER-001"):
    return {
        "idempotency_key": key, "producer": "order-service",
        "event_type": "OrderCreated", "schema_version": "1.0",
        "correlation_id": "CORR-ORDER-001",
        "payload": {"order_id": "ORD-1001", "amount": 125.0}
    }


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_message_publish_is_idempotent(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    first = client.post("/v1/messages", json=sample_message()).json()
    second = client.post("/v1/messages", json=sample_message()).json()
    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert first["message"]["id"] == second["message"]["id"]


def test_message_delivers_and_consumer_deduplicates(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/messages", json=sample_message()).json()["message"]
    delivered = client.post(f"/v1/messages/{created['id']}/process", json={}).json()
    assert delivered["status"] == "DELIVERED"
    assert delivered["attempts"] == 1
    duplicate = client.post(f"/v1/messages/{created['id']}/process", json={})
    assert duplicate.status_code == 409


def test_retry_exhaustion_routes_to_dead_letter_and_replay(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/messages", json=sample_message()).json()["message"]
    message_id = created["id"]
    for _ in range(3):
        result = client.post(f"/v1/messages/{message_id}/process", json={"simulate_failure": True})
    assert result.json()["status"] == "DEAD_LETTER"
    assert result.json()["attempts"] == 3
    assert len(client.get("/v1/dead-letters").json()) == 1
    replayed = client.post(f"/v1/dead-letters/{message_id}/replay")
    assert replayed.status_code == 200
    assert replayed.json()["status"] == "PENDING"
    delivered = client.post(f"/v1/messages/{message_id}/process", json={})
    assert delivered.json()["status"] == "DELIVERED"


def test_invalid_event_contract_is_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    payload = sample_message()
    payload["event_type"] = "UnknownEvent"
    response = client.post("/v1/messages", json=payload)
    assert response.status_code == 422


def test_message_delivery_audit_is_retained(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/messages", json=sample_message()).json()["message"]
    client.post(f"/v1/messages/{created['id']}/process", json={})
    events = client.get(f"/v1/messages/{created['id']}/audit").json()
    assert [event["action"] for event in events] == ["MESSAGE_ACCEPTED", "DELIVERY_SUCCEEDED"]


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401

