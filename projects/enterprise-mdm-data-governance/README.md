# Enterprise MDM and Data Governance

**Purpose:** Create trusted, consistent master records for suppliers, customers, products and locations across disconnected enterprise systems.

**Domain:** Master data management, data quality, stewardship and governance.  
**Technology direction:** API-based domain services, relational persistence, configurable matching and survivorship rules; concrete implementation choices will be recorded as architecture decisions.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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
The documents define the intended design and acceptance criteria. No live MDM deployment, data-quality improvement or enterprise source connection is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.
