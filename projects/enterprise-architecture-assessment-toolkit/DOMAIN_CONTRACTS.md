# Assessment, Stakeholder, Capability, ValueStream, Application, Interface, DataDomain, Technology, Gap, Option, Initiative, Decision — Domain Contracts and Data Model

> Proposed contract baseline. These endpoints, event names and entities require implementation and contract-test verification before they are treated as stable interfaces.

## Component interaction

```mermaid
flowchart TD
  A[Source or assessor input] --> B[API and contract validation]
  B --> C[Domain services]
  C --> D[Rules and workflow]
  D --> E[Persistence and lineage]
  C --> F[Event or downstream adapter]
  F --> G[Human review or consumer]
  E --> H[Audit and observability]
```

## Project workflow

Scope and drivers -> stakeholder concerns -> capability/value-stream baseline -> information/application/integration/technology inventory -> evidence-backed gaps -> options/trade-offs -> dependency roadmap -> governance decision

## Domain entities

- **POST /v1/assessments; POST /v1/inventory; POST /v1/gaps; POST /v1/options; GET /v1/roadmaps/{id}; POST /v1/decisions; GET /v1/evidence/{id}** — stable identifier, lifecycle state, timestamps, ownership and source/version references as applicable.

Preserve source keys, raw input references, versioned derived values and decision history. Use explicit relationships and constraints; avoid destructive updates to source evidence.

## Proposed REST API

- `AssessmentOpened, BaselineCaptured, GapRecorded, OptionEvaluated, RoadmapPublished, ArchitectureDecisionRecorded`

Common API rules:
- OpenAPI 3.x is the source of truth for request and response shapes.
- Use 201 for created resources, 202 for asynchronous work, 404 for unknown resources, 409 for invalid state transitions and 422 for validation errors.
- Include correlation_id in error responses and logs; use idempotency keys for retryable commands.
- Paginate collection endpoints, use UTC timestamps and stable enum values.

## Proposed domain events

- `Every assessment score links to criteria and evidence. Unknowns remain visible. Roadmap sequencing exposes dependencies` — include event_id, occurred_at, producer, subject, correlation_id and schema_version.
- `value` — include event_id, occurred_at, producer, subject, correlation_id and schema_version.
- `risk and accountable owner; no implied certification.` — include event_id, occurred_at, producer, subject, correlation_id and schema_version.

Consumers must be idempotent and tolerate duplicate delivery. Define ordering, replay and schema-compatibility expectations per stream.

## Business invariants and policy

undefined

## Security and data handling

- Authenticate callers and authorize each resource/action.
- Validate payload size, schema, state transitions and source authenticity where applicable.
- Store secrets outside the repository; use managed identity or short-lived credentials in deployed environments.
- Encrypt sensitive payloads and redact sensitive fields from logs/traces.
- Audit administrative actions, policy changes, approvals, replay and exports.
- Treat uploaded/retrieved content, tool output and event payloads as untrusted.
- Use synthetic fixtures in the public repository.

## Contract and data tests

- [ ] OpenAPI schema validation for every request and response.
- [ ] Required/optional fields, enum values, bounds and malformed payloads.
- [ ] Referential integrity and uniqueness constraints.
- [ ] Duplicate command/event and idempotent retry.
- [ ] Invalid state transition returns stable conflict response.
- [ ] Authorization denial and resource isolation.
- [ ] Event replay preserves business invariants.
- [ ] Audit links actor, action, resource, timestamp and correlation ID.
- [ ] Sensitive data is absent from logs and sample fixtures.

## Implementation note

This file specifies intended contracts; it does not assert that these endpoints, events or persistence models are implemented. Keep status in README aligned with code and test evidence.
