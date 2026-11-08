# Code Review

Review guidance for assessing changes in correctness, maintainability, security and operational suitability.

## Where the reviews will be applied

- [Spring PetClinic service enhancement](../projects/java-spring-petclinic/README.md): API behaviour, validation, persistence, transaction boundaries and regression risk.
- [Python batch data pipeline](../projects/python-batch-data-pipeline/README.md): malformed input, schema drift, idempotency, partial failures and safe logging.
- [Data quality framework](../projects/data-quality-framework/README.md): rule correctness, null handling, threshold semantics and rejected-record traceability.
- [AI agent evaluation workbench](../projects/ai-agent-evaluation-workbench/README.md): prompt/task reproducibility, provenance of changes and validity of evaluation evidence.
- [Quality automation pipeline](../projects/quality-automation-pipeline/README.md): CI permissions, secret handling, dependency checks and trustworthy test reporting.

## Review checklist

- Does the change meet the stated requirement and acceptance criteria?
- Are edge cases, null/empty values and invalid inputs handled?
- Does the change preserve existing behaviour where required?
- Are error handling and logging useful without exposing secrets or sensitive data?
- Are authorization, input validation and data access handled safely?
- Are tests meaningful and do they cover failure paths?
- Is the implementation consistent with the project's conventions?
- Are performance implications and resource usage reasonable?
- Are configuration, migration and deployment impacts documented?
- Can another engineer understand and maintain the change?

## Review outcome

Classify findings by severity and explain the impact, evidence and suggested correction. Separate blocking defects from recommendations and stylistic preferences.

## AI-generated changes

Review AI-generated code to the same standard as human-written code. Never treat generated explanations or claimed test results as evidence; inspect the diff and run checks independently.

## Status

Review checklist established. Project-specific reviews will be added only after implementation diffs and verification evidence exist.
