# Predictive Life Sciences Supply Chain

**Purpose:** Improve visibility of material availability, lot status and delivery risk across regulated life-sciences supply chains.

**Domain:** Life-sciences operations, supply chain analytics and predictive risk.  
**Technology direction:** Domain APIs, event ingestion, governed analytical data and explainable risk models; implementation choices will be recorded as ADRs.  
**Status:** CI + Docker build verified — 8 tests passed on Python 3.12 (GitHub Actions run 42477970815, commit 3ba8ab0). Authentication is enforced for protected API routes; the test suite includes a missing-key rejection check. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Represent materials, suppliers, purchase orders, inventory, lots and shipments.
- Ingest ERP, WMS, manufacturing, quality and logistics events.
- Track lot genealogy, expiry, quality holds and release status.
- Identify shortages, delays and material constraints.
- Calculate explainable risk indicators and scenario impacts.
- Present planner work queues and recommended next actions.

## Reference workflow
Operational source events → canonical supply-chain model → lot and order reconciliation → availability calculation → risk feature generation → prediction/scenario analysis → planner review → action and outcome capture.

## Key modules
- **Domain model:** material, supplier, order, lot, shipment and site.
- **Ingestion:** synthetic ERP/WMS/MES/QMS and logistics adapters.
- **Traceability:** lot genealogy, status and event history.
- **Planning:** demand/supply balance, constraints and exception queues.
- **Risk analytics:** delay/shortage features and explainable risk scoring.
- **Planner workflow:** review, action assignment and outcome feedback.

## Expected demonstration
Use synthetic pharmaceutical supply data to identify a lot on quality hold that affects a planned production order, calculate downstream shortage exposure and route the issue to a planner.

## Guardrails
Preserve lot-level traceability and data provenance. Predictions support planning decisions; they do not release batches, change quality status or replace authorised quality processes.

## First executable slice

The current prototype accepts synthetic material/lot availability inputs, calculates days of cover and projected quantity at replenishment, flags quality holds and pre-replenishment shortages, assigns explainable P1–P3 risk bands, persists scenarios and records an assessment audit event. It includes API tests, OpenAPI, a synthetic fixture, Docker and GitHub Actions.

**Limitations:** risk scoring is deterministic and illustrative, not a trained or validated predictive model. There are no ERP/WMS/MES/QMS/logistics connectors, lot genealogy, batch release workflow, demand forecast, supplier lead-time model, GxP validation, access controls or production data. Recommendations are planner guidance only and never change quality status or release material. GitHub Actions executed the API suite successfully: 8 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. Synthetic data only.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn lifesupply.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml). Synthetic example: [examples/synthetic-supply-scenario.json](examples/synthetic-supply-scenario.json).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
Use synthetic data and clearly labelled simulated events. No validated GxP system, regulated production use or forecast accuracy is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
