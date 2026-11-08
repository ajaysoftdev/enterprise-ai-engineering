from fastapi.testclient import TestClient
from dataprotection.main import app
from dataprotection import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "protection.db"))


def register_dataset():
    return client.post("/v1/datasets", json={
        "name": "synthetic-customer-ledger", "owner": "finance-data-owner",
        "purpose": "invoice-processing",
        "fields": [
            {"name": "customer_name", "classification": "PERSONAL"},
            {"name": "email", "classification": "PERSONAL"},
            {"name": "phone", "classification": "PERSONAL"},
            {"name": "account_number", "classification": "FINANCIAL"},
            {"name": "invoice_total", "classification": "FINANCIAL"},
            {"name": "region", "classification": "INTERNAL"}
        ]
    })


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_dataset_registration_and_retrieval(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = register_dataset()
    assert created.status_code == 201
    fetched = client.get(f"/v1/datasets/{created.json()['id']}")
    assert fetched.status_code == 200
    assert len(fetched.json()["fields"]) == 6


def test_analyst_allowed_only_masked_data(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    dataset = register_dataset().json()
    response = client.post("/v1/access/evaluate", json={
        "dataset_id": dataset["id"], "actor": "analyst@example.test",
        "role": "data-analyst", "purpose": "analytics",
        "requested_fields": ["customer_name", "region"], "mode": "MASKED"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "ALLOW"
    assert response.json()["masking_required"] is True


def test_finance_operator_cannot_read_personal_fields(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    dataset = register_dataset().json()
    response = client.post("/v1/access/evaluate", json={
        "dataset_id": dataset["id"], "actor": "finance@example.test",
        "role": "finance-operator", "purpose": "invoice-processing",
        "requested_fields": ["account_number", "customer_name"], "mode": "RAW"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "DENY"
    assert response.json()["allowed_fields"] == ["account_number"]


def test_wrong_purpose_is_denied(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    dataset = register_dataset().json()
    response = client.post("/v1/access/evaluate", json={
        "dataset_id": dataset["id"], "actor": "analyst@example.test",
        "role": "data-analyst", "purpose": "marketing",
        "requested_fields": ["region"], "mode": "MASKED"
    })
    assert response.json()["decision"] == "DENY"


def test_masking_preserves_only_safe_suffix_and_email_domain(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    dataset = register_dataset().json()
    response = client.post(f"/v1/datasets/{dataset['id']}/mask", json={"records": [{
        "customer_name": "Synthetic Customer", "email": "customer@example.test",
        "phone": "9876543210", "account_number": "123456789012",
        "invoice_total": "2500.00", "region": "North"
    }]})
    assert response.status_code == 200
    record = response.json()["records"][0]
    assert record["customer_name"] == "***MASKED***"
    assert record["email"] == "c***@example.test"
    assert record["phone"] == "***3210"
    assert record["account_number"] == "********9012"
    assert record["region"] == "North"


def test_policy_evaluation_is_audited(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    dataset = register_dataset().json()
    client.post("/v1/access/evaluate", json={
        "dataset_id": dataset["id"], "actor": "analyst@example.test",
        "role": "data-analyst", "purpose": "analytics",
        "requested_fields": ["region"], "mode": "MASKED"
    })
    events = client.get(f"/v1/datasets/{dataset['id']}/audit").json()
    assert len(events) == 1
    assert events[0]["decision"] == "ALLOW"


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401

