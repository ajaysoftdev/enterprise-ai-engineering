from fastapi.testclient import TestClient
from rndspine.main import app
from rndspine import repository

client = TestClient(app)


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "rnd.db"))


def record(source_id, kind, payload, parents=None):
    return {
        "source_system": "SYNTHETIC-LIMS", "source_record_id": source_id,
        "study_id": "STUDY-SYN-01", "record_type": kind,
        "record_name": source_id, "schema_version": "1.0",
        "parent_record_ids": parents or [], "payload": payload
    }


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_research_record_ingestion_and_lineage(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    experiment = client.post("/v1/records", json=record("EXP-1", "EXPERIMENT", {"protocol_id": "PROTO-1"})).json()
    sample = client.post("/v1/records", json=record("SAMPLE-1", "SAMPLE", {"material_id": "MAT-1"}, [experiment["id"]])).json()
    result = client.post("/v1/records", json=record(
        "RESULT-1", "ASSAY_RESULT",
        {"sample_id": sample["id"], "method_id": "METHOD-1", "result_value": 4.2, "unit": "mg/L"},
        [sample["id"]]
    )).json()
    assert result["status"] == "ACCEPTED"
    lineage = client.get(f"/v1/records/{result['id']}/lineage").json()
    assert {item["id"] for item in lineage["upstream_records"]} == {experiment["id"], sample["id"]}


def test_missing_scientific_metadata_is_quarantined(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/records", json=record("RESULT-2", "ASSAY_RESULT", {"result_value": 3.1}))
    assert response.status_code == 201
    assert response.json()["status"] == "QUARANTINED"
    assert len(response.json()["quality_issues"]) == 3


def test_missing_parent_is_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/records", json=record("SAMPLE-2", "SAMPLE", {"material_id": "MAT-2"}, ["missing-parent"]))
    assert response.status_code == 409


def test_duplicate_source_identifier_is_rejected(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    payload = record("EXP-2", "EXPERIMENT", {"protocol_id": "PROTO-2"})
    assert client.post("/v1/records", json=payload).status_code == 201
    assert client.post("/v1/records", json=payload).status_code == 409


def test_ingestion_audit_is_available(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/records", json=record("EXP-3", "EXPERIMENT", {"protocol_id": "PROTO-3"})).json()
    events = client.get(f"/v1/records/{created['id']}/audit").json()
    assert events[0]["action"] == "RECORD_ACCEPTED"


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32
