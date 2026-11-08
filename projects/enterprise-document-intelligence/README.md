# Enterprise Document Intelligence

## Purpose

A document intake and validation demonstrator that receives synthetic plain-text business documents, extracts labelled fields with evidence, applies deterministic validation and supports a recorded human review decision.

## Current implementation status

**Prototype code added — execution not yet verified**

The first executable slice is now present:
- FastAPI service with health, document create/list/read and review endpoints
- SQLite persistence for document metadata and extracted fields
- Deterministic labelled-field extraction for sample invoice-like text
- Required-field validation and NEEDS_REVIEW routing
- API tests, Dockerfile, Docker Compose profile and synthetic sample input

**Important limitations:** this version accepts only text/plain input. It does not yet parse PDF/image files, call an OCR or LLM provider, authenticate users, implement tenant isolation, publish events, or provide production-grade file storage. The tests have been added but have not yet been executed in CI or against a local runtime. Do not treat this prototype as production-ready or as a validated document-processing control.

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
  "text_content": "Supplier: Northwind Supplies\nInvoice Number: INV-2026-0042\nDate: 2026-11-08\nTotal: USD 1250.00"
}
```

## Next implementation milestones

1. Execute tests and fix any failures.
2. Add authentication, authorization, audit events and idempotency.
3. Add file quarantine, file-size limits, MIME/signature checks and malware scanning.
4. Add OCR adapter interfaces and a PDF/image processing path.
5. Add explicit field-level evidence locations, extraction versioning and review history.
6. Add PostgreSQL/object-storage adapters, retention controls and observability.
7. Add CI, dependency scanning and security tests.

## Project documentation

- [Implementation architecture](IMPLEMENTATION_ARCHITECTURE.md)
- [Reference sources](SOURCES.md)
- [Project blueprint](docs/PROJECT_BLUEPRINT.md)

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
