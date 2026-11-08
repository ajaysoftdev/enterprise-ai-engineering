# Enterprise Portfolio Integration — Domain Contracts

## Domain entities

- IntegrationWorkflow: orchestration aggregate with stable ID, workflow type, state and correlation ID.
- IdempotencyRecord: request key and canonical payload hash.
- DocumentReference: ID and validation outcome returned by Document Intelligence.
- SupplierSourceReference: source-system key and MDM source-record ID.
- MatchReference: MDM candidate ID and current stewardship status.
- GoldenRecordReference: MDM golden-record ID and canonical supplier identity.
- WorkflowAuditEvent: actor, action, state transition, downstream reference and UTC timestamp.

## Initial REST contract

| Method | Path | Purpose |
|---|---|---|
| POST | /v1/supplier-onboarding | Start idempotent supplier invoice workflow |
| GET | /v1/workflows/{workflow_id} | Read workflow state and references |
| POST | /v1/workflows/{workflow_id}/refresh | Refresh MDM stewardship outcome |
| POST | /v1/workflows/{workflow_id}/retry | Explicit retry after downstream state reconciliation |
| GET | /v1/workflows/{workflow_id}/audit | Read workflow audit events |
| GET | /health | Health check |

## Downstream contracts

Document Intelligence:
- POST /v1/documents with filename, content_type=text/plain and text_content.
- Response supplies document ID, status, extracted field values, confidence and evidence.

MDM:
- POST /v1/source-records with source_system, source_key, legal_name, tax_id and optional email.
- Response supplies source-record ID and either a golden-record ID or pending match-candidate ID.
- GET /v1/match-candidates returns stewardship status.
- GET /v1/golden-records returns golden records and source-record membership.

## State invariants

- One idempotency key maps to one canonical request hash and one workflow.
- Same key and same payload returns the original workflow.
- Same key and different payload returns a conflict.
- MDM match candidates are never auto-approved by the integration service.
- COMPLETED requires a downstream golden-record reference.
- WAITING_FOR_STEWARD requires a match-candidate reference.
- DOWNSTREAM_FAILED cannot be reported as completed.
- Every state transition appends an audit event.

## Event contract (future)

Proposed events: SupplierOnboardingRequested, DocumentValidated, SupplierSourceRecordCreated, SupplierMatchAwaitingSteward, SupplierGoldenRecordPublished, SupplierOnboardingFailed.

These events are proposed names only; the initial vertical slice uses synchronous HTTP adapters.
