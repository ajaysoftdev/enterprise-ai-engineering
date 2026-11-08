# Cloud Data Engineering Platform

**Purpose:** Provide a repeatable foundation for reliable ingestion, transformation, quality enforcement, lineage and cost-aware data delivery.

**Domain:** Cloud data engineering, lakehouse architecture and data operations.  
**Technology direction:** Python-based pipeline components, object-storage/lakehouse patterns, SQL transformations and orchestration adapters; concrete services will be selected through ADRs.  
**Status:** Current prototype CI + Docker verified — 7 tests passed on Python 3.12 (GitHub Actions run 42461086770, commit 05b8198). This verifies the synthetic prototype scope only; production readiness is not claimed.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Ingest batch and incremental data from files, APIs and databases.
- Define and validate data contracts at ingestion boundaries.
- Separate raw, standardised and curated data zones.
- Apply transformation, deduplication and schema evolution rules.
- Run data quality checks and quarantine invalid records.
- Track lineage, freshness, pipeline health and processing cost.
- Publish curated datasets for BI, analytics and AI workloads.

## Reference workflow
Source → landing/raw → contract validation → bronze/silver/gold transformations → quality gates → curated serving → lineage, metrics and cost monitoring.

## Key modules
- **Connectors:** batch, API and CDC-style ingestion adapters.
- **Contracts:** schema definitions, compatibility and validation.
- **Transformations:** reusable SQL/Python processing components.
- **Quality:** completeness, uniqueness, validity and reconciliation checks.
- **Orchestration:** dependencies, retries, backfills and run state.
- **Governance and FinOps:** lineage, access, freshness and cost attribution.

## Expected demonstration
Ingest synthetic sales and product files, validate schemas, quarantine malformed rows, transform curated outputs and inspect lineage and pipeline run metrics.

## Guardrails
Keep raw data immutable, make processing idempotent, protect sensitive fields and record schema changes. Avoid hard-coding cloud credentials or claiming cloud deployment before it is verified.

## First executable slice

The current prototype accepts synthetic sales rows, persists idempotent pipeline runs, validates required fields and value ranges, quarantines malformed/duplicate rows, calculates curated silver-level line totals and produces a product-level gold summary. It includes API tests, OpenAPI, synthetic input, Docker and a GitHub Actions workflow.

**Limitations:** this is a local SQLite/Python demonstration, not a cloud deployment or distributed lakehouse. There are no S3/ADLS connectors, Spark/Databricks, ADF/Airflow orchestration, CDC, schema registry, incremental checkpoints, immutable bronze object storage, access governance, lineage service, observability or FinOps measurement. GitHub Actions executed the API suite successfully: 6 passed, 0 failed. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. No scale or performance claim is made.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn cloudpipeline.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml). Synthetic input: [examples/synthetic-sales.json](examples/synthetic-sales.json).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No cloud account deployment, measured performance or production data pipeline is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
