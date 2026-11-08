# Enterprise Portfolio Integration — Implementation Architecture

## Architecture style

A modular integration orchestrator with provider-neutral HTTP adapters and a local durable workflow repository. Domain services remain autonomous owners of their records and decisions.

## Initial vertical slice

Supplier invoice onboarding:
- Integration API receives a document reference, text content, source-system identity and idempotency key.
- Document Intelligence extracts invoice fields and evidence.
- Integration validates the supplier name and tax identifier required by MDM.
- MDM creates a source record and either creates a golden record or returns a pending match candidate.
- Integration records COMPLETED or WAITING_FOR_STEWARD.
- A steward resolves the candidate through MDM; integration refreshes the workflow and records the final result.

## Logical components

1. API boundary: request validation, idempotency and correlation ID.
2. Workflow coordinator: explicit state transitions and downstream sequencing.
3. Document adapter: maps integration commands to Document Intelligence API.
4. MDM adapter: maps validated supplier data to MDM API and handles candidate/golden-record outcomes.
5. Repository: SQLite workflow, idempotency hash, references and audit events.
6. Refresh operation: queries MDM candidate/golden-record state after human stewardship.
7. Operational surface: health, workflow status and workflow audit.

## State model

RECEIVED → DOCUMENT_SUBMITTED → DOCUMENT_REVIEW_REQUIRED or MDM_SUBMITTED → WAITING_FOR_STEWARD or COMPLETED.

A workflow can move from WAITING_FOR_STEWARD to COMPLETED after an MDM CONFIRMED decision, or to STEWARD_REJECTED after a rejected match creates a separate golden record. Downstream errors are recorded as DOWNSTREAM_FAILED; an operator may retry through an explicit retry endpoint after checking the downstream state.

## Failure and consistency

- Each downstream operation uses a stable source key derived from the workflow request.
- The integration idempotency key is unique and payload-hash checked.
- Downstream services are authoritative; the integration repository stores IDs and a compact result snapshot.
- A network timeout is ambiguous: before retrying, the adapter must query the downstream service by stable key where supported.
- The initial implementation returns a downstream failure state and does not automatically retry ambiguous writes.
- Human stewardship remains in MDM; integration cannot approve a match.
- Reconciliation refreshes candidate status and retrieves the golden record by source-record membership.

## Security and operational controls

Current slice: schema validation, bounded payload sizes, safe request IDs, no-store response headers, parameterised SQLite statements, idempotency and append-only audit API.

Required before external exposure: service authentication, object-level authorization, tenant isolation, TLS, secret manager, rate limits, retry budgets, audit protection, metrics/traces, backup/restore and threat testing.

## Deployment topology

Local development uses three separate FastAPI processes:
- Document Intelligence: port 8001.
- MDM: port 8002.
- Portfolio Integration: port 8003.

Docker Compose for the integration service expects the domain services to be reachable through configurable URLs. It does not provision or claim to deploy the other projects automatically.

## Acceptance criteria

- Valid synthetic invoice creates a document and MDM source record.
- Missing supplier or tax ID pauses the workflow for document review.
- Duplicate idempotency key and same payload returns the existing workflow.
- Same key with a different payload returns 409.
- MDM match candidate pauses for stewardship.
- Confirmed or rejected steward outcome is reflected after refresh.
- Downstream timeout is recorded without silently marking the workflow complete.
- Workflow audit captures each transition and downstream reference.
