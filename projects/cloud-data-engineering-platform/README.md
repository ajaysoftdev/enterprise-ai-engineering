# Cloud Data Engineering Platform

**Purpose:** Provide a repeatable foundation for reliable ingestion, transformation, quality enforcement, lineage and cost-aware data delivery.

**Domain:** Cloud data engineering, lakehouse architecture and data operations.  
**Technology direction:** Python-based pipeline components, object-storage/lakehouse patterns, SQL transformations and orchestration adapters; concrete services will be selected through ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No cloud account deployment, measured performance or production data pipeline is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.
