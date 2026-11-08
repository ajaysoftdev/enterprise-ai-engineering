# Enterprise Portfolio Integration

**Purpose:** Connect the fifteen independently implemented enterprise prototypes through versioned contracts, provider-neutral adapters, durable workflow state and end-to-end traceability.

**Status:** First vertical slice CI + Docker verified — 10 tests passed on Python 3.12 (GitHub Actions run 42462133940, commit 3f3db89). This verifies orchestration state, idempotency and fake-adapter tests; the actual downstream HTTP integration still requires a three-service local end-to-end run.

## Initial vertical slice

1. Accept a synthetic supplier invoice and idempotency key.
2. Submit the text to Enterprise Document Intelligence.
3. Validate supplier name and supplier tax identifier from extracted evidence.
4. Submit a source record to Enterprise MDM and Data Governance.
5. Complete automatically only when MDM creates a new golden record.
6. Pause when MDM identifies a possible match; a data steward must decide in the MDM service.
7. Refresh the integration workflow after the steward decision and record the resulting golden-record reference.

## Architecture boundaries

- Domain services remain owners of their own data and business rules.
- Integration uses HTTP adapters and explicit mapping; it never writes directly to another project's database.
- The workflow stores references and state, not copies of all downstream domain data.
- Idempotency prevents duplicate workflow creation for the same request key and payload.
- A changed payload with an existing key returns a conflict.
- A pending MDM match is never auto-approved.
- The first slice uses synthetic plain-text invoices and configurable local service endpoints only. Automated tests use fake downstream adapters; they do not yet prove live HTTP interoperability between the three processes.

## Current limitations

No production API gateway, enterprise identity provider, tenant isolation, event broker, schema registry, distributed tracing backend, secrets manager, cloud deployment, dead-letter queue or cross-service compensation is implemented yet. HTTP calls have bounded timeouts but no automatic retry in this first slice. The service is not production-ready.

## Local run

The integration service expects Document Intelligence at http://localhost:8001 and MDM at http://localhost:8002.

Run each service from its project directory, then run this project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn portfolio_integration.main:app --reload --app-dir src --port 8003
pytest -q
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Documentation

- [Project blueprint](docs/PROJECT_BLUEPRINT.md)
- [Implementation architecture](IMPLEMENTATION_ARCHITECTURE.md)
- [Domain contracts](DOMAIN_CONTRACTS.md)
- [Reference sources](SOURCES.md)
- [Source layout](src/README.md)
- [Test strategy](tests/README.md)
- [Operations](infra/README.md)
