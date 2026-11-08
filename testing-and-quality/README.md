# Testing and Quality

A practical record of test strategy, execution evidence and software-quality checks.

## Featured project

[Quality automation pipeline](../projects/quality-automation-pipeline/README.md)

A CI workflow specification that brings together Java and Python test execution, build validation, formatting/static checks and dependency hygiene. The pipeline must report only checks that actually ran and must not expose secrets.

## Test levels

- Unit tests for isolated business logic
- Integration tests for application components and persistence
- API and contract tests for service boundaries
- Regression tests for previously identified defects
- Static analysis and dependency/security checks where available
- Manual exploratory tests for user-facing workflows

## Project-specific test focus

- Java/Spring: controller behaviour, service rules, repository integration and API error cases.
- Python ingestion: valid and malformed files, missing columns, type conversion, duplicate records and partial failures.
- Data quality: nulls, uniqueness, ranges, referential checks, thresholds and rejected-record accounting.
- Agent evaluation: repeatable task setup, diff inspection and independent verification.

## Test evidence

For each run, record the commit or branch, environment, command, date, result, failures and relevant sanitised logs. Distinguish tests not run, tests blocked by environment, and tests that failed.

## Quality principles

- Establish a baseline before changing code.
- Add a regression test for a reproducible defect.
- Prefer deterministic tests and controlled test data.
- Do not report a test as passed unless it was executed successfully.
- Keep credentials, tokens and personal data out of source control and logs.

## Status

Strategy and project specification documented; no test execution is claimed at this stage.
