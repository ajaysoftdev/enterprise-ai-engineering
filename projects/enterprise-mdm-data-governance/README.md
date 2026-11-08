# Enterprise MDM and Data Governance

**Purpose:** Create trusted, consistent master records for suppliers, customers, products and locations across disconnected enterprise systems.

**Domain:** Master data management, data quality, stewardship and governance.  
**Technology direction:** API-based domain services, relational persistence, configurable matching and survivorship rules; concrete implementation choices will be recorded as architecture decisions.  
**Status:** CI + Docker build verified — 10 tests passed on Python 3.12 (GitHub Actions run 42478842872). Authentication rejects missing/incorrect keys and fails closed when the server key is not configured. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

The initial code slice provides:
- FastAPI health, source-record ingestion, candidate listing, steward decision and golden-record listing endpoints
- SQLite persistence for source records, match candidates, golden records and steward decisions
- Deterministic exact matching on normalized tax identifiers
- Human confirmation/rejection before a candidate is merged or kept separate
- Synthetic supplier fixtures, API tests and a GitHub Actions workflow

**Important limitations:** matching is exact normalized tax-ID comparison only; there is no fuzzy matching, configurable survivorship, source-system connector, event publishing, authentication, tenant isolation, authorization, unmerge/version history, production-grade audit integrity or enterprise data-quality profiling. GitHub Actions executed the API suite successfully: 9 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. This is a local demonstrator, not a production MDM platform.

## Business capabilities
- Ingest master records from ERP, CRM, procurement and operational systems.
- Standardise attributes and validate domain-specific rules.
- Detect exact and probable duplicates using configurable matching.
- Resolve golden records through survivorship and precedence policies.
- Route uncertain matches and changes to data stewards.
- Publish approved master data and retain lineage and audit history.

## Reference workflow
Source ingestion → standardisation → validation → candidate matching → survivorship → stewardship review → golden-record publication → downstream synchronisation.

## Key modules
- **Source adapters:** batch/API ingestion and source-system identity.
- **Data quality:** profiling, validation, normalisation and issue tracking.
- **Matching:** deterministic and configurable fuzzy matching.
- **Golden record:** merge, survivorship, versioning and relationship management.
- **Stewardship:** queues, approvals, merge/unmerge and exception handling.
- **Distribution:** outbound APIs/events and delivery reconciliation.

## Expected demonstration
Load synthetic supplier and product records from multiple sources, identify duplicates, compare candidate matches, approve a merge and trace the published golden record to its source records.

## Guardrails
Do not silently merge ambiguous records. Preserve source values, explain match decisions, support unmerge/correction and record steward identity and approval.

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The implementation is limited to the synthetic local workflow described above. No live MDM deployment, data-quality improvement or enterprise source connection is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local runtime

```bash
pip install -e ".[dev]"
uvicorn mdm.main:app --reload --app-dir src
pytest
```

Docker:

```bash
docker compose up --build
```

API contract: [openapi.yaml](openapi.yaml). Synthetic supplier examples: [examples/sample-suppliers.json](examples/sample-suppliers.json).


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
