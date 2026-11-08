from fastapi.testclient import TestClient
from mdm.main import app
from mdm import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "mdm-test.db"))


def source(source_key, tax_id, name="Northwind Supplies"):
    return {
        "source_system": "ERP", "source_key": source_key,
        "legal_name": name, "tax_id": tax_id,
        "email": "ap@example.test",
    }


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_first_source_creates_golden_record(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/source-records", json=source("SUP-1", "GST-AB1234"))
    assert response.status_code == 201
    body = response.json()
    assert body["match_candidate"] is None
    assert body["golden_record"]["source_record_ids"] == [body["source_record"]["id"]]


def test_exact_tax_id_match_requires_steward_decision(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    first = client.post("/v1/source-records", json=source("SUP-1", "GST-AB1234")).json()
    second = client.post("/v1/source-records", json=source("SUP-2", "gst ab-1234", "Northwind Ltd")).json()
    assert second["match_candidate"]["status"] == "PENDING"
    assert second["golden_record"] is None
    candidate_id = second["match_candidate"]["id"]
    decision = client.post(f"/v1/match-candidates/{candidate_id}/decision", json={
        "decision": "CONFIRM_MATCH", "steward": "steward@example.test",
        "note": "Exact normalized tax identifier reviewed",
    })
    assert decision.status_code == 200
    golden = client.get("/v1/golden-records").json()
    assert len(golden) == 1
    assert len(golden[0]["source_record_ids"]) == 2


def test_rejected_match_creates_separate_golden_record(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/source-records", json=source("SUP-1", "GST-AB1234"))
    second = client.post("/v1/source-records", json=source("SUP-2", "GST-AB1234", "Different Legal Name")).json()
    response = client.post(f"/v1/match-candidates/{second['match_candidate']['id']}/decision", json={
        "decision": "REJECT_MATCH", "steward": "steward@example.test",
        "note": "Identity conflict",
    })
    assert response.status_code == 200
    assert len(client.get("/v1/golden-records").json()) == 2


def test_duplicate_source_key_returns_conflict(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/source-records", json=source("SUP-1", "GST-AB1234"))
    response = client.post("/v1/source-records", json=source("SUP-1", "GST-CD5678"))
    assert response.status_code == 409


def test_unknown_candidate_returns_404(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/match-candidates/not-found/decision", json={
        "decision": "CONFIRM_MATCH", "steward": "steward@example.test"
    })
    assert response.status_code == 404


def test_second_steward_decision_is_rejected_without_partial_change(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/source-records", json=source("SUP-1", "GST-AB1234"))
    second = client.post("/v1/source-records", json=source("SUP-2", "GST-AB1234", "Northwind Ltd")).json()
    candidate_id = second["match_candidate"]["id"]
    body = {
        "decision": "CONFIRM_MATCH", "steward": "steward@example.test",
        "note": "Reviewed exact identifier",
    }
    assert client.post(f"/v1/match-candidates/{candidate_id}/decision", json=body).status_code == 200
    repeated = client.post(f"/v1/match-candidates/{candidate_id}/decision", json=body)
    assert repeated.status_code == 409
    golden = client.get("/v1/golden-records").json()
    assert len(golden) == 1
    assert len(golden[0]["source_record_ids"]) == 2


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32
