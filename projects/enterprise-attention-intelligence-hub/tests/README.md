# Test strategy — Enterprise Attention and Intelligence Hub

## Test layers
1. **Unit:** domain invariants, state transitions, scoring/matching/policy rules and error cases.
2. **Application:** use-case orchestration with fake repositories and adapter ports.
3. **Contract:** request/response schemas, API compatibility, event schemas and consumer expectations.
4. **Integration:** persistence transactions, migrations, message delivery and adapter behaviour.
5. **End-to-end:** synthetic scenario covering Signal intake → normalisation → capability/service mapping → correlation → impact scoring → work queue → decision/outcome.
6. **Security:** auth boundaries, invalid input, injection surfaces, secret leakage, audit integrity and sensitive-data handling.
7. **Resilience:** timeouts, retry exhaustion, duplicate/out-of-order messages, dependency outage and partial failure.

## Synthetic fixtures
Generate synthetic examples for Signal, Metric, BusinessCapability, Service, Dependency, Correlation, ImpactAssessment, WorkItem, Decision, Outcome. Include valid, invalid, duplicate, incomplete and boundary cases. Do not use customer, patient, employee, vendor or production records.

## Definition of done
- Every business rule has positive and negative unit tests.
- API/event contracts have schema validation.
- Critical persistence paths test rollback and idempotency.
- End-to-end scenario is repeatable from a clean local environment.
- CI retains test reports; failures are not silently ignored.
- Performance thresholds are declared before performance claims.

## Current executable test slice
The current API suite covers health, high- and low-priority scoring, correlation of related signals across services, operator acknowledgement and duplicate acknowledgement conflict. It does not test real monitoring integrations, time-window correlation, SLOs, escalation delivery, access control or load behaviour.

## Evidence record
For each run record commit, runtime/tool versions, command, result, test count and exclusions. Until executed, a test is **planned**, not passed.
