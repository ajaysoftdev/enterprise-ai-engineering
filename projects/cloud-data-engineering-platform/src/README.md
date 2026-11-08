# Source-code layout — Cloud Data Engineering Platform

```text
src/
  cloudpipeline/
    main.py              # pipeline run and retrieval API
    models.py            # batch request and run-result contracts
    transform.py         # deterministic validation, quarantine, silver and gold transforms
    repository.py        # SQLite run metadata and output snapshots
  app/                  # config, composition, health
  contracts/            # versioned schemas and data contracts
  domain/
    entities.py         # Source, Pipeline, Dataset, DataContract, Run, Checkpoint, QualityResult, LineageNode, CostRecord
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
