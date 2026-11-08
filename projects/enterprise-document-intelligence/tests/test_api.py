from fastapi.testclient import TestClient
from docintel.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_retrieve_document(tmp_path, monkeypatch):
    from docintel import repository
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "test.db"))
    payload = {
        "filename": "sample-invoice.txt",
        "content_type": "text/plain",
        "text_content": "Supplier: Northwind Supplies\nInvoice Number: INV-2026-0042\nDate: 2026-11-08\nTotal: USD 1250.00",
    }
    created = client.post("/v1/documents", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["extracted_fields"]["document_number"]["value"] == "INV-2026-0042"
    assert body["extracted_fields"]["total_amount"]["value"] == "USD 1250.00"
    assert body["status"] == "RECEIVED"

    fetched = client.get(f"/v1/documents/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_missing_required_fields_routes_to_review(tmp_path, monkeypatch):
    from docintel import repository
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "review.db"))
    response = client.post("/v1/documents", json={
        "filename": "incomplete.txt",
        "content_type": "text/plain",
        "text_content": "Supplier: Example Vendor",
    })
    assert response.status_code == 201
    assert response.json()["status"] == "NEEDS_REVIEW"
    assert "Missing required field: document_number" in response.json()["validation_errors"]


def test_review_decision_is_persisted(tmp_path, monkeypatch):
    from docintel import repository
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "decision.db"))
    created = client.post("/v1/documents", json={
        "filename": "invoice.txt",
        "content_type": "text/plain",
        "text_content": "Invoice Number: INV-1\nTotal: 42.00",
    }).json()
    reviewed = client.post(f"/v1/documents/{created['id']}/review", json={
        "decision": "APPROVED",
        "reviewer": "reviewer@example.test",
        "note": "Synthetic test approval",
    })
    assert reviewed.status_code == 200
    assert reviewed.json()["status"] == "APPROVED"
    assert client.get(f"/v1/documents/{created['id']}").json()["reviewed_by"] == "reviewer@example.test"


def test_unknown_document_returns_404(tmp_path, monkeypatch):
    from docintel import repository
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "missing.db"))
    response = client.get("/v1/documents/not-a-real-id")
    assert response.status_code == 404


def test_audit_records_intake_and_review(tmp_path, monkeypatch):
    from docintel import repository
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "audit.db"))
    created = client.post("/v1/documents", json={
        "filename": "audit-sample.txt",
        "content_type": "text/plain",
        "text_content": "Invoice Number: AUD-7\nTotal: 17.00",
    }).json()
    reviewed = client.post(f"/v1/documents/{created['id']}/review", json={
        "decision": "APPROVED", "reviewer": "reviewer@example.test", "note": "Checked sample"
    })
    assert reviewed.status_code == 200
    events = client.get(f"/v1/documents/{created['id']}/audit").json()
    assert [event["action"] for event in events] == ["DOCUMENT_RECEIVED", "REVIEW_APPROVED"]
