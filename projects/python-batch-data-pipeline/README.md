# Project 2: Python Batch Data Pipeline

- Status: Proposed
- Type: Original portfolio exercise
- Data: Synthetic CSV and JSON files

## Problem context

Enterprise teams often receive files from different systems with inconsistent field names, missing values, invalid types and duplicate records. A small pipeline should make ingestion and transformation predictable and auditable.

## Proposed flow

```text
CSV / JSON inputs
      |
      v
File discovery and configuration
      |
      v
Schema and record validation
      |
      +---- invalid records ----> rejected-records output
      |
      v
Normalization and transformation
      |
      v
Deduplication / idempotency check
      |
      v
Accepted output + run summary
```

## Functional scope

- Read a configured input directory containing CSV and JSON files.
- Normalize source-specific field names into a canonical record structure.
- Validate required fields, data types, date formats and allowed values.
- Separate accepted and rejected records with reason codes.
- Handle empty files, malformed files and missing columns without losing the run context.
- Produce a summary with input, accepted, rejected and duplicate counts.
- Log processing stages without exposing sensitive record values.

## Non-functional scope

- Deterministic output for identical inputs and configuration.
- Clear exit codes and actionable error messages.
- Configurable paths and rules; no secrets in source control.
- Unit tests for parsing, validation, transformation and failure paths.
- Idempotent reruns for the same input batch.

## Acceptance criteria

- Sample CSV and JSON inputs produce the documented canonical output.
- Invalid records are quarantined with field-level reasons.
- A malformed file is reported and does not silently appear successful.
- Duplicate handling is deterministic and documented.
- Summary counts reconcile to the input records.
- Unit tests cover valid, invalid, empty and edge-case inputs.
- Run instructions work from a clean checkout.

## Suggested implementation sequence

1. Define canonical schema and synthetic sample data.
2. Implement parsers and configuration.
3. Implement pure validation and transformation functions.
4. Add rejected-record output and run summary.
5. Add CLI entry point and logging.
6. Add tests and a concise architecture/data-flow note.

## Deliverables

Python source, sample data, tests, run instructions, example output and a short review report. No cloud service is required for the first version.
