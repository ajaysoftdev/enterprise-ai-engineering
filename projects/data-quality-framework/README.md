# Project 3: Data Quality Framework

- Status: Proposed
- Type: Original portfolio exercise
- Data: Synthetic customer and order datasets

## Problem context

A pipeline can complete technically while still producing unreliable data. This project defines reusable checks and a report that makes data quality visible before downstream consumption.

## Quality dimensions

- Completeness: required fields and null thresholds.
- Validity: types, formats, ranges and allowed values.
- Uniqueness: duplicate business keys.
- Consistency: cross-field and cross-record rules.
- Referential integrity: order references to known customers.
- Timeliness: optional event or update timestamp freshness.

## Proposed flow

```text
Dataset + data contract
        |
        v
Schema / profiling
        |
        v
Rule execution
        |
        +---- failed rows ----> quarantine with rule IDs
        |
        v
Dataset scorecard + run report
```

## Functional scope

- Define a small declarative data contract for each dataset.
- Profile row count, null counts, distinct counts and basic ranges.
- Execute reusable field-level and dataset-level rules.
- Support configurable warning and failure thresholds.
- Produce row-level failure details and a dataset-level summary.
- Return a non-zero process status when configured critical rules fail.

## Acceptance criteria

- The same input and contract produce deterministic results.
- Every failed row is traceable to one or more rule identifiers.
- Summary counts reconcile with input and quarantine outputs.
- Warning and failure thresholds behave as documented.
- Missing columns and invalid contract definitions are handled explicitly.
- Tests cover each quality dimension and threshold boundary.

## Deliverables

Rule schema, synthetic datasets, validation engine, report output, tests, run instructions and example scorecard.

## Out of scope for the first increment

A production data catalog, enterprise MDM platform, distributed processing engine or machine-learning anomaly detector. These can be considered only after the core rules engine is verified.
