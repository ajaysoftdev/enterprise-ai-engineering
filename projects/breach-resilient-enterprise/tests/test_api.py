from fastapi.testclient import TestClient
from breach.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_compromised_contractor_reaches_sensitive_resources():
    response = client.get("/v1/attack-paths/contractor-temp")
    assert response.status_code == 200
    body = response.json()
    assert "customer-db" in body["reachable_sensitive_targets"]
    assert "secrets-vault" in body["reachable_sensitive_targets"]
    assert all(path["risk"] == "HIGH" for path in body["paths"])


def test_unknown_principal_has_no_paths():
    response = client.get("/v1/attack-paths/unknown-user")
    assert response.status_code == 200
    assert response.json()["paths"] == []


def test_policy_defaults_to_deny_for_secret_access():
    response = client.post("/v1/policies/evaluate", json={
        "principal": "contractor-temp", "resource": "secrets-vault", "action": "read"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "DENY"


def test_containment_plan_requires_human_approval_and_is_dry_run():
    response = client.post("/v1/containment/plan", json={
        "principal": "contractor-temp", "incident_id": "INC-SYN-001"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "AWAITING_APPROVAL"
    assert body["execution_mode"] == "SIMULATION_ONLY"
    assert "No identity" in body["note"]


def test_approved_plan_still_does_not_execute_controls():
    response = client.post("/v1/containment/plan", json={
        "principal": "contractor-temp", "incident_id": "INC-SYN-002",
        "approved_by": "security-steward@example.test"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED_DRY_RUN"
    assert response.json()["execution_mode"] == "SIMULATION_ONLY"
