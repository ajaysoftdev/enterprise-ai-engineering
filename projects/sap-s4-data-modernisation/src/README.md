# Source-code layout — SAP S/4HANA Data Modernisation

```text
src/
  sapmodern/
    main.py              # migration batch intake, retrieval and report API
    models.py            # typed source-record and migration contracts
    mapping.py           # deterministic Business Partner/Material mapping and checks
    repository.py        # SQLite migration report and idempotency persistence
  app/                  # config, composition and health
  contracts/
    sap/                # SAP-facing interface schemas
    canonical/          # canonical data contracts
  domain/
    entities.py         # BusinessPartner, MaterialMaster, Plant, CompanyCode, SourceExtract, MappingRule, ChangeEvent, MigrationBatch, ReconciliationResult
    mapping_rules.py    # transformation definitions
    validation.py       # domain quality rules
  application/
    commands/           # extract, validate, steward, load, reconcile
    ports.py             # source/target adapter contracts
  infrastructure/
    adapters/           # sap_contracts, extract_adapter, cdc_adapter, canonical_mapping, validation, mdg_workflow, load_adapter, reconciliation, lineage, reporting
    persistence/        # migration state and audit
    simulators/         # synthetic SAP-like source/target
  reconciliation/       # counts, keys and attribute comparisons
  lineage/              # source-to-target provenance
  observability/        # logs, metrics and traces
```

## Engineering rules
- Use synthetic SAP-like payloads; do not claim live SAP connectivity.
- Keep source and target mappings versioned.
- Separate initial migration from incremental change processing.
- Quarantine invalid rows with reason codes.
- Make loads idempotent and reconcile after every batch.
- Preserve source keys and transformation version for lineage.

## First executable milestone
Implement synthetic source extract, canonical business partner mapping, validation rules, target simulator, reconciliation report and unit tests. Live SAP adapter is a separately scoped extension.
