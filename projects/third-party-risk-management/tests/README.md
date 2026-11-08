# Test strategy — Third-Party Risk Management

## Test layers
1. Unit: state machine, permissions, scoring and lifecycle rules.
2. Application: workflow orchestration with fake agents and repositories.
3. Contract: task, tool, evidence and API schema validation.
4. Integration: sandbox, Git adapter and persistence.
5. End-to-end: synthetic flow covering Vendor intake → inherent risk tiering → due diligence → control/evidence assessment → approval → access review → monitoring → offboarding.
6. Security: sandbox escape attempts, path traversal, tool misuse, secret exposure and privilege boundaries.
7. Resilience: timeout, cancellation, crash, retry, duplicate request and partial evidence.

## Fixtures
Create synthetic Vendor, Service, RiskTier, Assessment, Control, Evidence, Finding, Approval, AccessGrant, FourthParty, ReviewEvent fixtures. Include invalid permissions, malformed tasks, incomplete evidence and boundary budgets. Vendor workflow tests must use fictitious supplier records.

## Definition of done
Tasks are reproducible; tool policies are enforced; evidence is retained; scores can be recomputed from versioned rubrics; unsafe actions are blocked; CI retains test results.

## Current executable test slice
The current API suite covers health, high/low inherent-risk tiering, approval blocking until required evidence is current, expired-evidence rejection, evidence metadata submission and unknown-vendor handling. It does not verify evidence documents, real supplier feeds, access recertification, fourth-party graph completeness or external approval authority.

## Evidence
Record commit, environment, agent/model version when used, tool policy, command, budgets, results and exclusions. Untested scenarios remain planned.
