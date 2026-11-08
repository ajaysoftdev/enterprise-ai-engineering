# Test strategy — Enterprise Information Resilience

## Test layers
1. **Unit:** domain invariants, state transitions, scoring/matching/policy rules and error cases.
2. **Application:** use-case orchestration with fake repositories and adapter ports.
3. **Contract:** request/response schemas, API compatibility, event schemas and consumer expectations.
4. **Integration:** persistence transactions, migrations, message delivery and adapter behaviour.
5. **End-to-end:** synthetic scenario covering Signal intake → provenance assessment → claim/entity correlation → risk scoring → analyst review → approved response → audit.
6. **Security:** auth boundaries, invalid input, injection surfaces, secret leakage, audit integrity and sensitive-data handling.
7. **Resilience:** timeouts, retry exhaustion, duplicate/out-of-order messages, dependency outage and partial failure.

## Synthetic fixtures
Generate synthetic examples for Signal, Source, Claim, Entity, RiskAssessment, Case, ReviewDecision, ResponseAction, AuditEvent. Include valid, invalid, duplicate, incomplete and boundary cases. Do not use customer, patient, employee, vendor or production records.

## Definition of done
- Every business rule has positive and negative unit tests.
- API/event contracts have schema validation.
- Critical persistence paths test rollback and idempotency.
- End-to-end scenario is repeatable from a clean local environment.
- CI retains test reports; failures are not silently ignored.
- Performance thresholds are declared before performance claims.

## Current executable test slice
The current API suite covers health, explainable signal scoring, shared-case grouping, human review, prevention of repeat review and audit events. It does not test real source monitoring, semantic claim matching, factual verification, identity resolution, source authenticity or response publishing.

## Evidence record
For each run record commit, runtime/tool versions, command, result, test count and exclusions. Until executed, a test is **planned**, not passed.
