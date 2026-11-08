# Pharma R&D Data Spine

**Purpose:** Establish traceable links across research, laboratory, formulation, manufacturing and clinical data so scientific evidence can be discovered and interpreted in context.

**Domain:** Pharmaceutical R&D data architecture, scientific traceability and governed analytics.  
**Technology direction:** Metadata-driven ingestion, domain contracts, lineage and governed data products; implementation choices will be documented as ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

## Business capabilities
- Register studies, experiments, samples, materials, methods and batches.
- Ingest metadata from ELN, LIMS, formulation, MES and clinical-like sources.
- Resolve identities and relationships across systems.
- Track sample, method, experiment and batch lineage.
- Apply data quality, provenance and access controls.
- Publish curated, traceable research datasets for analytics.

## Reference workflow
Source registration → metadata ingestion → identity resolution → schema and quality validation → relationship/lineage construction → governed data product → scientific discovery and audit.

## Key modules
- **Source registry:** system, dataset, owner and refresh metadata.
- **Scientific model:** study, experiment, sample, material, method and batch.
- **Identity resolution:** cross-system identifiers and mapping rules.
- **Lineage:** transformation and evidence relationships.
- **Governance:** quality rules, access, classification and audit.
- **Data products:** curated datasets and documented interfaces.

## Expected demonstration
Load synthetic experiment, sample and assay records from separate systems, resolve their identifiers and trace a reported result back to its source sample, method and experiment.

## Guardrails
Do not fabricate scientific observations or alter source evidence. Preserve provenance, version transformations and distinguish synthetic demonstration records from regulated records.

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
Use synthetic research data. No validated laboratory integration, regulatory qualification or clinical decision support is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
