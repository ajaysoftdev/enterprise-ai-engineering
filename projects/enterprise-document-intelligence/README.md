# Enterprise Document Intelligence
**Latest revision verified:** Supplier tax-identifier extraction and its integration handoff test passed in the latest CI run.

## Purpose

A document intake and validation demonstrator that receives synthetic plain-text business documents, extracts labelled fields with evidence, applies deterministic validation and supports a recorded human review decision.

## Current implementation status

**Status:** CI + Docker build verified — 9 tests passed on Python 3.12 (GitHub Actions run 42478818147). Authentication rejects missing/incorrect keys and fails closed when the server key is not configured. This verifies synthetic/local prototype behaviour only, not production readiness.

The first executable slice is now present:
- FastAPI service with health, document create/list/read, review and audit-read endpoints
- SQLite persistence for document metadata, extracted fields and append-only application audit events
- Deterministic labelled-field extraction for sample invoice-like text, including supplier tax identifier and evidence
- Required-field validation and NEEDS_REVIEW routing
- API tests, Dockerfile, Docker Compose profile and synthetic sample input

**Important limitations:** this version accepts only text/plain input. It does not yet parse PDF/image files, call an OCR or LLM provider, authenticate users, implement tenant isolation or idempotency keys, publish events, or provide production-grade file storage. The audit table is append-only through this prototype API but is not tamper-proof against direct database modification. GitHub Actions executed the API suite successfully: 8 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. Do not treat this prototype as production-ready or as a validated document-processing control.

## Run locally

Requires Python 3.11 or later.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn docintel.main:app --reload --app-dir src
```

Open the interactive API docs at `http://127.0.0.1:8000/docs`.

Run tests:

```bash
pytest
```

Run with Docker:

```bash
docker compose up --build
```

## Sample request

```json
{
  "filename": "sample-invoice.txt",
  "content_type": "text/plain",
  "text_content": "Supplier: Northwind Supplies\nGSTIN: GST-AB1234\nInvoice Number: INV-2026-0042\nDate: 2026-11-08\nTotal: USD 1250.00"
}
```

## Next implementation milestones

1. Execute tests and fix any failures.
2. Add authentication, authorization, idempotency keys and stronger audit integrity controls.
3. Add file quarantine, file-size limits, MIME/signature checks and malware scanning.
4. Add OCR adapter interfaces and a PDF/image processing path.
5. Add explicit field-level evidence locations, extraction versioning and review history.
6. Add PostgreSQL/object-storage adapters, retention controls and observability.
7. Verify the configured CI workflow, then add dependency scanning and security tests.

## Project documentation

- [Implementation architecture](IMPLEMENTATION_ARCHITECTURE.md)
- [Reference sources](SOURCES.md)
- [OpenAPI contract](openapi.yaml)
- [Project blueprint](docs/PROJECT_BLUEPRINT.md)

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
