# SAP S/4HANA Data Modernisation

**Purpose:** Demonstrate governed master-data migration and synchronisation patterns between SAP-like source domains, modern platforms and analytics consumers.

**Domain:** SAP S/4HANA data architecture, migration, data quality and integration.  
**Technology direction:** Synthetic SAP-like extracts, mapping/validation services, API or CDC-style adapters and reconciliation controls. No live SAP connection is assumed.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

## Business capabilities
- Model representative business partners, products/materials and organisational data.
- Ingest synthetic source extracts and change events.
- Map legacy structures to target domain contracts.
- Validate mandatory fields, code lists and cross-object dependencies.
- Detect duplicates and route ambiguous records to stewardship.
- Load target-shaped records and reconcile counts and values.
- Preserve migration lineage, exceptions and restartability.

## Reference workflow
SAP-like extract/change event → staging → mapping and validation → duplicate resolution/stewardship → target load/API → reconciliation → lineage and exception reporting.

## Key modules
- **Source simulator:** representative SAP-style master and transactional records.
- **Mapping catalogue:** source-to-target field mappings and transformation rules.
- **Validation:** mandatory fields, referential integrity and domain checks.
- **Migration orchestration:** batch, checkpoints, restart and error handling.
- **Reconciliation:** count, amount, key and sample-level comparisons.
- **Governance:** ownership, lineage, approvals and exception reporting.

## Expected demonstration
Migrate synthetic business-partner and material records, inject invalid and duplicate records, resolve exceptions and produce a reconciliation report with traceable source-to-target mappings.

## Guardrails
Do not imply access to SAP systems or SAP certification. Use synthetic SAP-like data, document assumptions and keep migration execution separate from reconciliation approval.

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No SAP tenant integration, production migration or customer data processing is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
