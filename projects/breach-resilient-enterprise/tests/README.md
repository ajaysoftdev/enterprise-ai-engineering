# Test strategy — Breach-Resilient Enterprise

## Test layers
1. **Unit:** domain invariants, state transitions, scoring/matching/policy rules and error cases.
2. **Application:** use-case orchestration with fake repositories and adapter ports.
3. **Contract:** request/response schemas, API compatibility, event schemas and consumer expectations.
4. **Integration:** persistence transactions, migrations, message delivery and adapter behaviour.
5. **End-to-end:** synthetic scenario covering Threat scenario → identity event → policy evaluation → workload/API checks → data control → detection → response → recovery.
6. **Security:** auth boundaries, invalid input, injection surfaces, secret leakage, audit integrity and sensitive-data handling.
7. **Resilience:** timeouts, retry exhaustion, duplicate/out-of-order messages, dependency outage and partial failure.

## Synthetic fixtures
Generate synthetic examples for Asset, Identity, TrustBoundary, ThreatScenario, Control, Finding, Incident, ResponsePlaybook, Evidence. Include valid, invalid, duplicate, incomplete and boundary cases. Do not use customer, patient, employee, vendor or production records.

## Definition of done
- Every business rule has positive and negative unit tests.
- API/event contracts have schema validation.
- Critical persistence paths test rollback and idempotency.
- End-to-end scenario is repeatable from a clean local environment.
- CI retains test reports; failures are not silently ignored.
- Performance thresholds are declared before performance claims.

## Current executable test slice
The current API tests cover health, sensitive-target reachability from a synthetic compromised identity, unknown-principal behaviour, default-deny secret access, human approval gating and the guarantee that containment remains simulation-only. Real identity, network, workload, cloud and SOC integrations are not tested.

## Evidence record
For each run record commit, runtime/tool versions, command, result, test count and exclusions. Until executed, a test is **planned**, not passed.
