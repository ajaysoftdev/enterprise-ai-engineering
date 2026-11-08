from fastapi.testclient import TestClient
from sapmodern.main import app
from sapmodern import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "sap.db"))


def payload(key="MIG-001", records=None):
    return {
        "idempotency_key": key, "source_system": "SYNTHETIC-SAP-ERP",
        "mapping_version": "2026.1",
        "records": records or [
            {"record_type": "BUSINESS_PARTNER", "source_key": "BP-100",
             "payload": {"name": "Northwind Ltd", "country": "in", "tax_id": "GST-100"}},
            {"record_type": "MATERIAL_MASTER", "source_key": "MAT-200",
             "payload": {"material_code": "MAT-200", "description": "Sterile Vial", "base_uom": "ea", "plant": "p100"}}
        ]
    }


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_valid_records_map_to_canonical_target(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/migrations", json=payload())
    assert response.status_code == 201
    migration = response.json()["migration"]
    assert migration["status"] == "RECONCILED"
    assert migration["loaded_count"] == 2
    assert migration["loaded_records"][0]["country_code"] == "IN"
    assert migration["loaded_records"][1]["base_unit"] == "EA"


def test_invalid_records_are_quarantined_and_reconciled(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    body = payload(records=[
        {"record_type": "BUSINESS_PARTNER", "source_key": "BP-1", "payload": {"name": "Vendor"}},
        {"record_type": "MATERIAL_MASTER", "source_key": "MAT-1", "payload": {"description": "Vial"}}
    ])
    migration = client.post("/v1/migrations", json=body).json()["migration"]
    assert migration["loaded_count"] == 0
    assert migration["quarantined_count"] == 2
    assert migration["count_reconciled"] is True
    assert migration["status"] == "RECONCILED_WITH_EXCEPTIONS"


def test_duplicate_source_keys_are_quarantined(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    body = payload(records=[
        {"record_type": "BUSINESS_PARTNER", "source_key": "BP-DUP",
         "payload": {"name": "Vendor A", "country": "US", "tax_id": "T1"}},
        {"record_type": "BUSINESS_PARTNER", "source_key": "BP-DUP",
         "payload": {"name": "Vendor B", "country": "US", "tax_id": "T2"}}
    ])
    migration = client.post("/v1/migrations", json=body).json()["migration"]
    assert migration["loaded_count"] == 1
    assert migration["quarantined_count"] == 1


def test_migration_submission_is_idempotent(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    first = client.post("/v1/migrations", json=payload()).json()
    second = client.post("/v1/migrations", json=payload()).json()
    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert first["migration"]["id"] == second["migration"]["id"]


def test_migration_report_is_retrievable(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/migrations", json=payload()).json()["migration"]
    response = client.get(f"/v1/migrations/{created['id']}")
    assert response.status_code == 200
    assert response.json()["mapping_version"] == "2026.1"


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401

