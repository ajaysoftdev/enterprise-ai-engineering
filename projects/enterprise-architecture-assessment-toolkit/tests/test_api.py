from fastapi.testclient import TestClient
from eatoolkit.main import app
from eatoolkit import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "ea.db"))


def assessment_payload():
    return {
        "assessment_name": "Synthetic Commerce Architecture Review",
        "business_objectives": ["Improve order visibility", "Reduce integration duplication"],
        "capabilities": [
            {"name": "Order Management", "current_maturity": 2, "target_maturity": 4,
             "evidence_references": ["synthetic://interviews/order-team"]},
            {"name": "Integration", "current_maturity": 1, "target_maturity": 4,
             "evidence_references": ["synthetic://application-inventory"]},
            {"name": "Data Governance", "current_maturity": 3, "target_maturity": 4}
        ],
        "dependencies": [
            {"source_capability": "Order Management", "target_capability": "Integration", "relationship": "DEPENDS_ON"},
            {"source_capability": "Integration", "target_capability": "Data Governance", "relationship": "DUPLICATES"},
            {"source_capability": "Unknown", "target_capability": "Data Governance", "relationship": "SUPPORTS"}
        ]
    }


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_assessment_calculates_maturity_gaps_and_roadmap(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/assessments", json=assessment_payload())
    assert response.status_code == 201
    report = response.json()
    assert report["overall_current_maturity"] == 2.0
    assert report["overall_target_maturity"] == 4.0
    assert report["roadmap"][0]["capability"] == "Integration"
    assert report["roadmap"][0]["priority"] == "HIGH"


def test_duplicate_capability_names_are_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    payload = assessment_payload()
    payload["capabilities"].append(payload["capabilities"][0])
    response = client.post("/v1/assessments", json=payload)
    assert response.status_code == 422


def test_dependency_duplication_and_unresolved_references_are_flagged(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    report = client.post("/v1/assessments", json=assessment_payload()).json()
    findings = [item["finding"] for item in report["dependency_findings"]]
    assert "POTENTIAL_CAPABILITY_DUPLICATION" in findings
    assert "UNRESOLVED_CAPABILITY_REFERENCE" in findings


def test_assessment_report_is_persisted(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/assessments", json=assessment_payload()).json()
    fetched = client.get(f"/v1/assessments/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["assessment_name"] == created["assessment_name"]


def test_missing_assessment_returns_404(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    assert client.get("/v1/assessments/not-found").status_code == 404


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32
