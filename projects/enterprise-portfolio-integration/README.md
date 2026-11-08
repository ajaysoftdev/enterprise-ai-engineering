# Enterprise Portfolio Integration

**Purpose:** Connect the fifteen independently implemented enterprise prototypes through versioned contracts, provider-neutral adapters, durable workflow state and end-to-end traceability.

**Status:** First vertical slice CI + Docker + real HTTP E2E + security verified — 12 tests passed on Python 3.12 (GitHub Actions run 42478610123, commit 7fa4c4a). The integration API now requires an API key and forwards distinct downstream keys to Document Intelligence and MDM.. The workflow starts Document Intelligence, MDM and Integration as separate HTTP services, exercises the steward decision and refresh path, and builds the integration Docker image.

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
- The first slice uses synthetic plain-text invoices and configurable local service endpoints only. Unit tests use fake downstream adapters; a separate GitHub Actions smoke test starts all three services and exercises the real HTTP handoff, idempotency, MDM stewardship and refresh flow. The three-service smoke test has passed in GitHub Actions. URL-scheme restrictions, parameterised workflow updates, Bandit and pip-audit also passed in security matrix run 42478610160 (16/16 project jobs).


## Three-service end-to-end run

Install the three packages from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e "projects/enterprise-document-intelligence[dev]" -e "projects/enterprise-mdm-data-governance[dev]" -e "projects/enterprise-portfolio-integration[dev]"
```

Start these services in separate terminals from the repository root:

```bash
uvicorn docintel.main:app --reload --app-dir projects/enterprise-document-intelligence/src --port 8001
uvicorn mdm.main:app --reload --app-dir projects/enterprise-mdm-data-governance/src --port 8002
uvicorn portfolio_integration.main:app --reload --app-dir projects/enterprise-portfolio-integration/src --port 8003
```

Then run from this project directory:

```bash
pytest -q
python scripts/e2e_smoke.py
```

Docker: `docker compose up --build` (the two domain services must already be reachable on the configured host URLs). API contract: [openapi.yaml](openapi.yaml).

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


## API authentication and local secrets

All non-health endpoints require an API key. Copy `.env.example` to `.env` and set three distinct secrets: `API_KEY` for this integration API, `DOCINT_API_KEY` matching the Document Intelligence service key, and `MDM_API_KEY` matching the MDM service key. Keep populated `.env` files out of source control. The HTTP adapters forward the appropriate downstream key; CI uses disposable test-only keys.
