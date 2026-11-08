"""Three-service HTTP smoke test for the supplier onboarding vertical slice."""
import json
import os
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.getenv("INTEGRATION_URL", "http://127.0.0.1:8003")


def call(path: str, method: str = "GET", payload: dict | None = None, headers: dict | None = None, base: str = BASE):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request_headers = {"Accept": "application/json"}
    service_key = os.getenv("API_KEY")
    if service_key:
        request_headers["X-API-Key"] = service_key
    if body is not None:
        request_headers["Content-Type"] = "application/json"
    request_headers.update(headers or {})
    request = Request(base.rstrip("/") + path, data=body, method=method, headers=request_headers)
    try:
        with urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read() or b"{}")
    except HTTPError as exc:
        return exc.code, json.loads(exc.read() or b"{}")


def wait_for_services():
    for _ in range(45):
        try:
            if call("/health")[0] == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Integration API did not become healthy")


def invoice(source_key: str, number: str, supplier: str):
    return {
        "source_system": "PROCUREMENT",
        "source_key": source_key,
        "filename": f"{number}.txt",
        "text_content": (
            f"Supplier: {supplier}\n"
            "GSTIN: GST-AB1234\n"
            f"Invoice Number: {number}\n"
            "Date: 2026-11-08\n"
            "Total: USD 125.00\n"
        ),
    }


def main():
    wait_for_services()

    key = "e2e-invoice-001"
    first_payload = invoice("SUP-E2E-001", "INV-E2E-001", "Northwind Supplies")
    status, first = call("/v1/supplier-onboarding", "POST", first_payload, {"Idempotency-Key": key, "X-Request-ID": "e2e-flow-001"})
    assert status == 202, first
    workflow = first["workflow"]
    assert workflow["state"] == "COMPLETED", workflow
    assert workflow["golden_record_id"], workflow
    assert workflow["correlation_id"] == "e2e-flow-001"

    duplicate_status, duplicate = call(
        "/v1/supplier-onboarding", "POST", first_payload, {"Idempotency-Key": key}
    )
    assert duplicate_status == 202, duplicate
    assert duplicate["duplicate"] is True
    assert duplicate["workflow"]["id"] == workflow["id"]

    second_payload = invoice("SUP-E2E-002", "INV-E2E-002", "Northwind Supplies Ltd")
    status, second = call(
        "/v1/supplier-onboarding", "POST", second_payload,
        {"Idempotency-Key": "e2e-invoice-002"},
    )
    assert status == 202, second
    waiting = second["workflow"]
    assert waiting["state"] == "WAITING_FOR_STEWARD", waiting
    assert waiting["match_candidate_id"], waiting

    decision_status, decision = call(
        f"/v1/match-candidates/{waiting['match_candidate_id']}/decision",
        "POST",
        {
            "decision": "CONFIRM_MATCH",
            "steward": "e2e-steward@example.test",
            "note": "Confirmed during synthetic integration smoke test",
        },
        headers={"X-API-Key": os.getenv("MDM_API_KEY", os.getenv("API_KEY", ""))},
        base=os.getenv("MDM_URL", "http://127.0.0.1:8002"),
    )
    assert decision_status == 200, decision

    refresh_status, refreshed = call(f"/v1/workflows/{waiting['id']}/refresh", "POST")
    assert refresh_status == 200, refreshed
    assert refreshed["state"] == "COMPLETED", refreshed
    assert refreshed["outcome"] == "MATCH_CONFIRMED", refreshed
    assert refreshed["golden_record_id"] == workflow["golden_record_id"]

    audit_status, events = call(f"/v1/workflows/{waiting['id']}/audit")
    assert audit_status == 200, events
    assert len(events) >= 3, events
    print("HTTP end-to-end smoke test passed: Document Intelligence -> MDM -> Portfolio Integration")


if __name__ == "__main__":
    main()
