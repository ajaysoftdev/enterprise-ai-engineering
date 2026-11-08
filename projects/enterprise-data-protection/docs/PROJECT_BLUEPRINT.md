# Enterprise Data Protection — Project Blueprint

**Status:** Architecture and implementation specification  
**Domain:** Data discovery, classification, minimisation and access governance  
**Primary stack:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, policy adapter, synthetic data

## Business problem
Apply consistent classification, purpose limitation, masking and auditable access across data copies and services.

## Intended users and outcomes
Provide business, operations, data, risk and engineering users with a repeatable, auditable capability. The solution must make decisions traceable and keep consequential actions reviewable.

## End-to-end reference flow
Dataset registration → discovery → classification → ownership/purpose → policy → masking → governed access → lineage/audit.

## Logical architecture
1. **Ingress/adapters:** isolate source-specific APIs, files, events and provider SDKs.
2. **Domain/application:** implement business rules and state transitions independently of transport.
3. **Persistence:** define identifiers, transaction boundaries, retention and reconciliation.
4. **Workflow:** model durable states, bounded retries, idempotency and dead-letter handling.
5. **Human control:** route low-confidence, high-impact or policy-restricted cases for review.
6. **Observability:** structured logs, metrics, traces, correlation IDs and operational events.
7. **Security:** least privilege, secret management, validation, audit and data minimisation.

## Domain model
Core entities: Dataset, DataElement, Classification, DataOwner, Purpose, AccessPolicy, MaskingRule, AccessRequest, AuditRecord. Define stable identifiers, lifecycle states, ownership, timestamps, provenance and relationships. Retain source identifiers alongside canonical identifiers for traceability.

## Code modules
Implement: catalog, discovery, classification, ownership, policy, masking, tokenization_adapter, access_gateway, lineage, audit. Transport handlers call application services; services coordinate domain rules and repositories; adapters translate external protocols into canonical contracts. Avoid business logic in controllers, notebooks or provider callbacks.

## Interfaces
- Versioned REST endpoints for synchronous commands and queries where appropriate.
- Versioned events for asynchronous state changes where appropriate.
- OpenAPI and, when events are used, AsyncAPI or equivalent schemas.
- Standard error envelopes, pagination, correlation IDs and idempotency headers.
- Provider-specific credentials and SDKs remain behind adapters.

## Security and governance
Threat-model authentication, authorisation, data boundaries, injection, sensitive-data exposure, supply-chain risk, abuse and audit integrity. Define retention/deletion behaviour. Use synthetic data in examples.

## Non-functional requirements
Set measurable targets during implementation for availability, latency/throughput, recovery, freshness, scalability and operating cost. Include tests for dependency outage, duplicate delivery, malformed input and partial completion.

## Delivery increments
1. Runnable skeleton, typed configuration, health endpoints, domain types and unit tests.
2. Core workflow and persistence with integration tests.
3. External adapters, API/event contracts and failure handling.
4. Security controls, observability, container deployment and CI.
5. Synthetic end-to-end demo, evaluation report and operations runbook.

## Acceptance criteria
- Clean checkout starts using documented commands.
- Core domain rules have deterministic automated tests.
- API/event contracts are versioned and validated.
- Failure handling, auditability and security controls have explicit tests.
- Synthetic end-to-end scenario is reproducible.
- Documentation distinguishes implemented, tested and pending capabilities.

## Project boundary
This project owns its domain capability and can be run independently. Cross-project orchestration, shared identity federation and portfolio-wide dashboards belong to the later integration project.
