from fastapi.testclient import TestClient
from cloudpipeline.main import app
from cloudpipeline import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "pipeline.db"))


def valid_row(order_id="ORD-1", product="SKU-1", quantity=2, price=10):
    return {
        "order_id": order_id, "product_id": product, "quantity": quantity,
        "unit_price": price, "event_date": "2026-11-08"
    }


def run_payload(key="BATCH-001", rows=None):
    return {"idempotency_key": key, "source_name": "synthetic-sales.csv",
            "rows": rows or [valid_row()]}


def test_health():
    response = client.get("/health", headers={"X-Request-ID": "test-request-01"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"] == "test-request-01"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_pipeline_transforms_silver_rows_and_gold_summary(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/pipelines/sales/run", json=run_payload(rows=[
        valid_row("ORD-1", "SKU-1", 2, 10), valid_row("ORD-2", "SKU-1", 3, 5)
    ]))
    assert response.status_code == 201
    run = response.json()["run"]
    assert run["accepted_count"] == 2
    assert run["curated_rows"][0]["line_total"] == 20
    assert run["gold_summary"] == [{"product_id": "SKU-1", "quantity": 5, "revenue": 35}]


def test_invalid_rows_are_quarantined(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/pipelines/sales/run", json=run_payload(rows=[
        valid_row(), {"order_id": "ORD-BAD", "quantity": -1}
    ]))
    run = response.json()["run"]
    assert run["accepted_count"] == 1
    assert run["quarantined_count"] == 1
    assert run["status"] == "COMPLETED_WITH_QUARANTINE"


def test_duplicate_order_ids_are_quarantined(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/pipelines/sales/run", json=run_payload(rows=[
        valid_row("ORD-DUP"), valid_row("ORD-DUP")
    ]))
    run = response.json()["run"]
    assert run["duplicate_count"] == 1
    assert run["accepted_count"] == 1
    assert run["quarantined_count"] == 1


def test_pipeline_submission_is_idempotent(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    first = client.post("/v1/pipelines/sales/run", json=run_payload()).json()
    second = client.post("/v1/pipelines/sales/run", json=run_payload()).json()
    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert first["run"]["id"] == second["run"]["id"]


def test_pipeline_run_can_be_retrieved(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = client.post("/v1/pipelines/sales/run", json=run_payload()).json()["run"]
    fetched = client.get(f"/v1/pipelines/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["raw_count"] == 1


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401

