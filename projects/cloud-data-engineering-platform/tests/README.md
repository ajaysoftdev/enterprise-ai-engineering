# Test strategy — Cloud Data Engineering Platform

## Test layers
1. Unit: canonicalisation, business rules, transformations and data-quality rules.
2. Contract: schema compatibility and required metadata.
3. Integration: local storage, database/catalog and orchestration adapters.
4. Pipeline: checkpointing, incremental rerun, replay and quarantine.
5. End-to-end: synthetic flow covering Source → landing/raw → contract validation → bronze/silver/gold transformations → quality gates → curated serving → lineage/metrics/cost.
6. Security: access boundaries, sensitive-data handling and secret leakage.
7. Resilience: malformed input, duplicates, late data, partial stage failure and dependency outage.

## Synthetic fixtures
Generate Source, Pipeline, Dataset, DataContract, Run, Checkpoint, QualityResult, LineageNode, CostRecord examples. Include missing identifiers, conflicting source values, invalid units, duplicate events and late-arriving records. Never use real patient or confidential research data.

## Definition of done
Schema checks run before processing; invalid rows are quarantined; reruns are idempotent; lineage is queryable; output is deterministic; CI retains test and quality reports.

## Evidence
Record commit, runtime versions, command, input fixture version, output counts, test results and exclusions. Untested checks remain planned.
