# Test strategy — Agent-Driven Enterprise Operations

## Test layers
1. Unit: domain invariants, lifecycle transitions and matching/policy rules.
2. Application: use-case orchestration with fake repositories and adapters.
3. Contract: API request/response schemas and event compatibility.
4. Integration: persistence, migrations, transactions and adapter behaviour.
5. End-to-end: synthetic flow covering Business event → workflow selection → agent plan → tool/policy validation → bounded execution → exception escalation → human decision → audit.
6. Security: authentication/authorisation, invalid input, injection, sensitive data, secret leakage and audit integrity.
7. Resilience: timeouts, retries, duplicate/out-of-order events, partial failure and dependency outage.

## Fixtures
Generate synthetic examples for Workflow, AgentRun, Plan, Tool, ToolPermission, PolicyDecision, ApprovalRequest, Task, Exception, RunEvidence, including valid, invalid, duplicate, incomplete and boundary cases. Never use production or personal data.

## Definition of done
Every business rule has positive and negative tests; contracts validate; critical writes test rollback and idempotency; end-to-end flow runs from a clean environment; CI retains test reports. Performance claims require declared thresholds and repeatable measurements.

## Evidence
Record commit, runtime/tool versions, command, result, test count and exclusions. Until executed, tests are planned, not passed.
