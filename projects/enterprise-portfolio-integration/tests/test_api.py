from fastapi.testclient import TestClient
from portfolio_integration.main import app
from portfolio_integration import repository
from portfolio_integration.adapters import AdapterError

client = TestClient(app)


class FakeDocumentAdapter:
    def __init__(self, response=None, error=None):
        self.response = response or {
            "id": "doc-001",
            "status": "RECEIVED",
            "validation_errors": [],
            "extracted_fields": {
                "supplier": {"value": "Northwind Supplies", "confidence": 0.9, "evidence": "Supplier: Northwind Supplies"},
                "supplier_tax_id": {"value": "GST-AB1234", "confidence": 0.9, "evidence": "GSTIN: GST-AB1234"},
                "document_number": {"value": "INV-1001", "confidence": 0.9, "evidence": "Invoice Number: INV-1001"},
                "total_amount": {"value": "1250.00", "confidence": 0.9, "evidence": "Total: 1250.00"},
            },
        }
        self.error = error
        self.calls = 0

    def submit(self, payload, request_id=None):
        self.calls += 1
        if self.error:
            raise self.error
        return self.response


class FakeMdmAdapter:
    def __init__(self, response=None, refresh_response=None):
        self.response = response or {
            "source_record": {"id": "source-001"},
            "match_candidate": None,
            "golden_record": {"id": "golden-001"},
        }
        self.refresh_response = refresh_response or {
            "candidate_status": "CONFIRMED",
            "golden_record_id": "golden-001",
        }
        self.calls = 0

    def create_supplier(self, payload, request_id=None):
        self.calls += 1
        self.payload = payload
        return self.response

    def refresh(self, candidate_id, source_record_id, request_id=None):
        self.refresh_args = (candidate_id, source_record_id)
        return self.refresh_response


def configure(tmp_path, monkeypatch, document=None, mdm=None):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "portfolio.db"))
    app.state.document_adapter = document or FakeDocumentAdapter()
    app.state.mdm_adapter = mdm or FakeMdmAdapter()


def request_body(text="Supplier: Northwind Supplies\nGSTIN: GST-AB1234\nInvoice Number: INV-1001\nTotal: 1250.00"):
    return {
        "source_system": "PROCUREMENT",
        "source_key": "SUP-1001",
        "filename": "invoice-1001.txt",
        "text_content": text,
    }


def test_health_and_request_context():
    response = client.get("/health", headers={"X-Request-ID": "integration-test-01"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "integration-test-01"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_valid_invoice_completes_document_to_mdm_flow(tmp_path, monkeypatch):
    mdm = FakeMdmAdapter()
    configure(tmp_path, monkeypatch, mdm=mdm)
    response = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1001"}, json=request_body())
    assert response.status_code == 202
    workflow = response.json()["workflow"]
    assert workflow["state"] == "COMPLETED"
    assert workflow["document_id"] == "doc-001"
    assert workflow["source_record_id"] == "source-001"
    assert workflow["golden_record_id"] == "golden-001"
    assert mdm.payload["legal_name"] == "Northwind Supplies"
    assert mdm.payload["tax_id"] == "GST-AB1234"


def test_missing_supplier_tax_id_pauses_for_document_review(tmp_path, monkeypatch):
    doc = FakeDocumentAdapter()
    doc.response["extracted_fields"]["supplier_tax_id"]["value"] = None
    mdm = FakeMdmAdapter()
    configure(tmp_path, monkeypatch, document=doc, mdm=mdm)
    response = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1002"}, json=request_body())
    assert response.status_code == 202
    assert response.json()["workflow"]["state"] == "DOCUMENT_REVIEW_REQUIRED"
    assert mdm.calls == 0


def test_idempotency_returns_existing_workflow_for_same_payload(tmp_path, monkeypatch):
    doc = FakeDocumentAdapter()
    configure(tmp_path, monkeypatch, document=doc)
    first = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1003"}, json=request_body())
    second = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1003"}, json=request_body())
    assert first.json()["workflow"]["id"] == second.json()["workflow"]["id"]
    assert second.json()["duplicate"] is True
    assert doc.calls == 1


def test_reused_idempotency_key_with_changed_payload_returns_conflict(tmp_path, monkeypatch):
    configure(tmp_path, monkeypatch)
    client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1004"}, json=request_body())
    changed = request_body(text="Supplier: Other Supplier\nGSTIN: GST-CD5678\nInvoice Number: INV-2\nTotal: 50.00")
    response = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1004"}, json=changed)
    assert response.status_code == 409


def test_possible_mdm_match_waits_for_steward_and_refreshes(tmp_path, monkeypatch):
    mdm = FakeMdmAdapter(
        response={
            "source_record": {"id": "source-002"},
            "match_candidate": {"id": "candidate-002", "status": "PENDING"},
            "golden_record": None,
        },
        refresh_response={"candidate_status": "CONFIRMED", "golden_record_id": "golden-002"},
    )
    configure(tmp_path, monkeypatch, mdm=mdm)
    started = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1005"}, json=request_body()).json()["workflow"]
    assert started["state"] == "WAITING_FOR_STEWARD"
    refreshed = client.post(f"/v1/workflows/{started['id']}/refresh")
    assert refreshed.status_code == 200
    assert refreshed.json()["state"] == "COMPLETED"
    assert refreshed.json()["outcome"] == "MATCH_CONFIRMED"
    assert mdm.refresh_args == ("candidate-002", "source-002")


def test_downstream_failure_is_recorded_not_marked_complete(tmp_path, monkeypatch):
    configure(tmp_path, monkeypatch, document=FakeDocumentAdapter(error=AdapterError("Document service unavailable")))
    response = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1006"}, json=request_body())
    assert response.status_code == 202
    assert response.json()["workflow"]["state"] == "DOWNSTREAM_FAILED"
    assert "Document service unavailable" in response.json()["workflow"]["error"]


def test_workflow_audit_records_transitions(tmp_path, monkeypatch):
    configure(tmp_path, monkeypatch)
    started = client.post("/v1/supplier-onboarding", headers={"Idempotency-Key": "invoice-1007"}, json=request_body()).json()["workflow"]
    events = client.get(f"/v1/workflows/{started['id']}/audit").json()
    assert [item["action"] for item in events] == ["WORKFLOW_CREATED", "STATE_TRANSITION"]


def test_unknown_workflow_returns_404(tmp_path, monkeypatch):
    configure(tmp_path, monkeypatch)
    assert client.get("/v1/workflows/missing").status_code == 404


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32
