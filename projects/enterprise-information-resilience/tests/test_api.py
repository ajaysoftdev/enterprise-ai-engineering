from fastapi.testclient import TestClient
from inforesilience.main import app
from inforesilience import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "info.db"))


def signal(source_id, **overrides):
    payload = {
        "case_key": "CASE-SYN-01", "source_id": source_id,
        "source_type": "PUBLIC_WEB", "evidence_reference": f"synthetic://{source_id}",
        "claim_text": "Synthetic claim used for resilience workflow testing",
        "source_reliability": 0.8, "reach": 4, "velocity": 3,
        "corroboration": 2, "business_impact": 4
    }
    payload.update(overrides)
    return payload


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_signal_is_scored_with_explainable_factors(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/signals", json=signal("SRC-1"))
    assert response.status_code == 201
    assert response.json()["risk_score"] == 72
    assert response.json()["priority"] == "P2"
    assert "source_reliability" in response.json()["risk_factors"]


def test_related_signals_are_grouped_into_a_case(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/signals", json=signal("SRC-1"))
    client.post("/v1/signals", json=signal("SRC-2", source_type="PARTNER", reach=5))
    case = client.get("/v1/cases/CASE-SYN-01").json()
    assert case["signal_count"] == 2
    assert case["source_count"] == 2
    assert case["risk_score"] > max(item["risk_score"] for item in case["signals"])


def test_human_review_is_required_and_no_external_response_runs(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/signals", json=signal("SRC-1"))
    response = client.post("/v1/cases/CASE-SYN-01/review", json={
        "reviewer": "communications-reviewer@example.test",
        "decision": "NEEDS_EVIDENCE", "rationale": "Seek another independent source"
    })
    assert response.status_code == 200
    assert response.json()["external_response_executed"] is False


def test_second_review_decision_is_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/signals", json=signal("SRC-1"))
    body = {"reviewer": "reviewer@example.test", "decision": "DISMISS", "rationale": "Insufficient corroboration"}
    client.post("/v1/cases/CASE-SYN-01/review", json=body)
    assert client.post("/v1/cases/CASE-SYN-01/review", json=body).status_code == 409


def test_case_audit_records_ingestion_and_review(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    client.post("/v1/signals", json=signal("SRC-1"))
    client.post("/v1/cases/CASE-SYN-01/review", json={
        "reviewer": "reviewer@example.test", "decision": "CONFIRM_RISK",
        "rationale": "Synthetic exercise only"
    })
    events = client.get("/v1/cases/CASE-SYN-01/audit").json()
    assert [item["event_type"] for item in events] == ["SIGNAL_INGESTED", "HUMAN_REVIEW_RECORDED"]
