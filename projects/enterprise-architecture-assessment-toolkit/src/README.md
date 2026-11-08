# Source-code layout — Enterprise Architecture Assessment Toolkit

```text
src/
  app/                  # config, composition and health
  contracts/
    sap/                # SAP-facing interface schemas
    canonical/          # canonical data contracts
  domain/
    entities.py         # Assessment, BusinessDriver, Capability, Process, InformationObject, Application, TechnologyComponent, Dependency, Gap, Option, RoadmapInitiative, Decision
    mapping_rules.py    # transformation definitions
    validation.py       # domain quality rules
  application/
    commands/           # extract, validate, steward, load, reconcile
    ports.py             # source/target adapter contracts
  infrastructure/
    adapters/           # assessment, capability_map, evidence, inventory, dependency_graph, gap_analysis, option_model, roadmap, adr, report_generator
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
