from datetime import date, timedelta
from fastapi.testclient import TestClient
from tprm.main import app
from tprm import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "tprm.db"))


def vendor(**overrides):
    payload = {
        "vendor_name": "Synthetic Cloud Provider", "service_name": "Document Hosting",
        "service_criticality": 5, "data_sensitivity": 5,
        "internet_facing": True, "privileged_access": True,
        "fourth_party_count": 4, "owner": "vendor-risk-team"
    }
    payload.update(overrides)
    return payload


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_high_risk_vendor_gets_high_tier(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/vendors", json=vendor())
    assert response.status_code == 201
    assert response.json()["risk_tier"] == "HIGH"
    assert response.json()["inherent_score"] == 98


def test_approval_blocked_until_required_evidence_is_current(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/vendors", json=vendor()).json()
    decision = client.post(f"/v1/vendors/{created['id']}/decision", json={
        "decision": "APPROVE", "approver": "risk-committee@example.test"
    })
    assert decision.status_code == 409
    for control in created["required_controls"]:
        client.post(f"/v1/vendors/{created['id']}/evidence", json={
            "control_id": control, "evidence_reference": f"synthetic://{control}",
            "valid_until": (date.today() + timedelta(days=90)).isoformat()
        })
    assessment = client.get(f"/v1/vendors/{created['id']}/assessment").json()
    assert assessment["evidence_complete"] is True
    approved = client.post(f"/v1/vendors/{created['id']}/decision", json={
        "decision": "APPROVE", "approver": "risk-committee@example.test"
    })
    assert approved.status_code == 200
    assert approved.json()["status"] == "APPROVED"


def test_expired_evidence_does_not_satisfy_control(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/vendors", json=vendor()).json()
    client.post(f"/v1/vendors/{created['id']}/evidence", json={
        "control_id": "access-control", "evidence_reference": "synthetic://expired",
        "valid_until": (date.today() - timedelta(days=1)).isoformat()
    })
    assessment = client.get(f"/v1/vendors/{created['id']}/assessment").json()
    assert "access-control" in assessment["missing_controls"]


def test_low_risk_vendor_requires_fewer_controls(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/vendors", json=vendor(
        service_criticality=1, data_sensitivity=1, internet_facing=False,
        privileged_access=False, fourth_party_count=0
    )).json()
    assert created["risk_tier"] == "LOW"
    assert created["required_controls"] == ["access-control"]


def test_unknown_vendor_returns_404(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    assert client.get("/v1/vendors/not-found").status_code == 404
