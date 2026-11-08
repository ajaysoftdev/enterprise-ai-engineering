# Portfolio Integration Contract Register

## Purpose and status

This register defines how the 15 independently implemented prototype projects should exchange information when a separate portfolio integration project is built. It is a proposed integration design, not evidence that the services are currently connected.

Each project owns its domain data and API. The current OpenAPI and domain-contract files are the source of truth for each prototype's existing routes. The interfaces below identify the cross-project handoffs still to standardise.

## Project-to-project handoff map

| Producer | Consumer | Business handoff | Preferred interaction | Required control |
|---|---|---|---|---|
| Enterprise MDM and Data Governance | Document Intelligence, SAP Modernisation, Pharma R&D Data Spine, Life Sciences Supply | Approved canonical supplier/product/site identity | Versioned API plus MasterRecordChanged event | Steward approval, source lineage, duplicate-safe upsert |
| Document Intelligence | MDM, Integration Platform, Agent Operations | Validated extracted document fields and exception status | API response and DocumentValidated event | Evidence pointer, confidence/validation result, human review |
| SAP S/4HANA Data Modernisation | MDM, Cloud Data Engineering, Integration Platform | Source mapping, migration batch and reconciliation result | Batch manifest, API and reconciliation event | Source-to-target traceability, count/value reconciliation, restartability |
| Cloud Data Engineering Platform | Pharma R&D Data Spine, Life Sciences Supply, Attention Hub | Curated data products, quality results and lineage | Data product contract and quality event | Schema version, quality gate, lineage and freshness |
| Pharma R&D Data Spine | Life Sciences Supply | Study, material, batch and provenance metadata | API/event contract | Synthetic-only in demo; controlled identifiers and lineage |
| Life Sciences Supply Chain | Attention Hub, Agent Operations, Integration Platform | Lot availability, supply risk and planner exception | Event plus query API | Explainable risk factors, no autonomous regulated action |
| Third-Party Risk Management | Agent Operations, Attention Hub, EA Assessment Toolkit | Vendor tier, evidence status, control gaps and remediation | API/event contract | Evidence provenance, review owner, expiry and access controls |
| Enterprise Data Protection | Document Intelligence, Cloud Data Engineering, MDM, Agent Operations | Classification, access and masking policy decisions | Policy decision API | Default deny on unknown policy; policy version and decision audit |
| Breach-Resilient Enterprise | Attention Hub, Agent Operations, Integration Platform | Simulated identity/asset risk and containment recommendation | Security event and case API | Simulation boundary; authorised approval for real containment |
| Agent-Driven Enterprise Operations | MDM, TPRM, Integration Platform, Document Intelligence | Approved workflow tasks, action requests and outcomes | Durable workflow/task API | Agent identity, tool allowlist, scoped permission and human approval |
| Autonomous AI Engineering Workbench | Engineering CI, Architecture Assessment Toolkit | Patch evaluation, test evidence and policy result | Signed evaluation report/artifact | Isolated execution, no production credentials, reproducible evidence |
| Enterprise Attention and Intelligence Hub | Agent Operations, EA Assessment Toolkit | Prioritised operational cases and business impact | Case API and notification event | Correlation ID, SLO/impact rationale, deduplication |
| Enterprise Information Resilience | Attention Hub, Agent Operations, EA Assessment Toolkit | Evidence-backed information-risk case and review decision | Case API and review event | Source provenance, uncertainty, legal/communications review; no automatic public response |
| Enterprise Integration Platform | All domain services | Routing, schema validation, retries, replay and delivery status | API gateway and event backbone | Idempotency, bounded retry, DLQ, schema compatibility and reconciliation |
| Enterprise Architecture Assessment Toolkit | All project owners | Capability, application, data, integration, risk and target-state evidence | Read-only inventory APIs and evidence register | Named accountable owner, evidence date, confidence and review cycle |

## Shared cross-project contracts

### 1. Event envelope

Every asynchronous event should carry:

- event_id: globally unique event identifier.
- event_type: stable domain event name.
- event_version: explicit schema version.
- occurred_at: UTC timestamp.
- producer: service and bounded environment identity.
- subject_id: domain entity or aggregate identifier.
- correlation_id: end-to-end business transaction identifier.
- causation_id: event or command that caused this event, when applicable.
- tenant_id: trusted tenant context established by the authenticated platform, never accepted as an authority claim from arbitrary payload data.
- data: versioned domain payload.
- sensitivity: classification label and handling constraints.

### 2. API conventions

- OpenAPI 3.x for synchronous HTTP APIs.
- Stable resource IDs and UTC timestamps.
- Consistent pagination, validation errors and conflict responses.
- Explicit idempotency-key behaviour for state-changing operations.
- Conditional updates or version fields where concurrent modification is possible.
- Correlation ID propagation across HTTP and asynchronous messages.
- No internal database tables exposed as public API contracts.

### 3. Identity and policy context

- User, service and agent identities must be distinct.
- The integration layer propagates verified identity claims; it must not invent roles or permissions.
- Consumers enforce object-level authorization independently.
- Policy decisions include policy ID/version, decision, rationale code and expiry.
- A failed or unavailable policy decision must not silently become allow.

### 4. Evidence and audit contract

- Evidence references identify a controlled object or immutable version, not just a free-form URL.
- Audit records include actor, action, target, timestamp, correlation ID and outcome.
- Sensitive values are excluded from routine logs.
- Consumers can trace a decision to the source event, source record and approving human where relevant.

### 5. Failure and delivery contract

- At-least-once event delivery is assumed unless a platform guarantee is explicitly documented.
- Consumers must be idempotent.
- Retry only transient failures, with bounded exponential backoff and jitter.
- Poison messages move to a controlled dead-letter queue with replay authorization.
- Reconciliation detects missing, duplicated and out-of-order business records.
- Human approval is required for irreversible or high-impact operations.

## Integration implementation sequence

1. Contract inventory: validate every project's current OpenAPI and domain contract; record implemented versus proposed fields.
2. Shared envelope: implement and test event, error, audit, identity and correlation schemas.
3. Adapter boundary: create provider-neutral ports and adapters for HTTP, event broker, database and file/object storage.
4. First vertical slice: Document Intelligence → MDM → Integration Platform using synthetic supplier invoice data, human approval and reconciliation.
5. Data lineage slice: Integration Platform → Cloud Data Engineering → Pharma R&D Data Spine with schema and quality gates.
6. Operational slice: Life Sciences Supply and Breach-Resilient simulation → Attention Hub → human-approved Agent Operations workflow.
7. Governance slice: TPRM, Data Protection and EA Assessment consume versioned evidence and policy decisions.
8. End-to-end verification: contract compatibility, idempotency, duplicate delivery, retries, DLQ replay, authorization, tenant isolation, audit, backup/restore and operational telemetry.

## Integration acceptance criteria

- Every producer and consumer has a named owner and versioned contract.
- No service writes directly to another service's database.
- Contract tests validate compatibility in CI.
- Duplicate delivery does not create duplicate business effects.
- Retries and replay are bounded and auditable.
- Authorization is enforced at the resource owner, not only at the gateway.
- High-impact actions have an explicit human approval record.
- End-to-end traces can be followed with a correlation ID.
- Reconciliation proves completeness for the chosen business flow.
- The integrated demonstration uses synthetic data and clearly states what is simulated.

## Current readiness

The 15 core prototypes have independent local APIs and domain contracts, but they are not yet connected through a common identity provider, event broker, API gateway, schema registry or shared audit service. The sixteenth Enterprise Portfolio Integration project now implements the first supplier-onboarding vertical slice across Document Intelligence and MDM. Its 10 unit tests, Docker build and a separate real-HTTP smoke test passed in GitHub Actions run 42462678787. The smoke test starts all three services, submits two invoices, confirms an MDM stewardship decision, refreshes the integration workflow and verifies the golden-record result. Broader cross-domain event-driven integration remains proposed. The broader event-driven and cross-domain integration roadmap remains proposed.
