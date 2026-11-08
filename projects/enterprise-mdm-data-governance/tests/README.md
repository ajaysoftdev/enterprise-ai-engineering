# Test strategy — Enterprise MDM and Data Governance

## Test layers
1. Unit: domain invariants, lifecycle transitions and matching/policy rules.
2. Application: use-case orchestration with fake repositories and adapters.
3. Contract: API request/response schemas and event compatibility.
4. Integration: persistence, migrations, transactions and adapter behaviour.
5. End-to-end: synthetic flow covering Source registration → ingestion → standardisation → candidate matching → survivorship → stewardship → golden record → distribution.
6. Security: authentication/authorisation, invalid input, injection, sensitive data, secret leakage and audit integrity.
7. Resilience: timeouts, retries, duplicate/out-of-order events, partial failure and dependency outage.

## Fixtures
Generate synthetic examples for SourceSystem, Party, Supplier, Customer, Product, Location, MatchCandidate, GoldenRecord, StewardshipCase, DataQualityResult, including valid, invalid, duplicate, incomplete and boundary cases. Never use production or personal data.

## Definition of done
Every business rule has positive and negative tests; contracts validate; critical writes test rollback and idempotency; end-to-end flow runs from a clean environment; CI retains test reports. Performance claims require declared thresholds and repeatable measurements.

## Current executable test slice
The current API suite covers health, initial golden-record creation, exact normalized tax-ID candidate creation, steward confirmation, steward rejection, duplicate source-key conflict and unknown-candidate handling. Tests use synthetic records and a temporary SQLite database. Authentication, tenant isolation, concurrency/race handling, rollback atomicity, fuzzy matching and event delivery are not covered yet.

## Evidence
Record commit, runtime/tool versions, command, result, test count and exclusions. Until executed, tests are planned, not passed.
