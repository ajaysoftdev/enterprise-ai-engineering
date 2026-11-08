# Source-code layout — Pharma R&D Data Spine

```text
src/
  rndspine/
    main.py              # record intake, lineage and audit API
    models.py            # typed research record and provenance contracts
    quality.py           # record-type-specific metadata checks
    repository.py        # SQLite records, lineage edges and audit persistence
  app/                  # config, composition, health
  contracts/            # versioned schemas and data contracts
  domain/
    entities.py         # Study, Experiment, Sample, Material, Method, Result, Formulation, Batch, Protocol, Dataset, LineageEdge
    rules.py            # domain invariants
    lineage.py          # provenance and dependency model
  ingestion/
    connectors/         # source adapters
    landing/            # immutable raw capture
    checkpoints.py      # incremental progress
  processing/
    standardize/        # canonicalisation
    transforms/         # bronze/silver/gold or equivalent
    quality/            # validation and quarantine
  catalog/              # metadata and ownership
  orchestration/        # pipeline state and scheduling adapter
  serving/              # curated outputs and APIs
  observability/        # logs, metrics, lineage events
```

## Engineering rules
- Keep raw source evidence immutable where the use case requires it.
- Validate schemas before transformation.
- Make pipeline stages restartable and idempotent.
- Quarantine invalid records with reason codes rather than silently dropping them.
- Record input/output dataset versions and lineage.
- Keep notebooks for exploration; production logic belongs in tested modules.

## First executable milestone
Implement one local file/source connector, a schema contract, a deterministic transformation, quality checks, checkpoint and unit tests. Cloud deployment is a later increment.
