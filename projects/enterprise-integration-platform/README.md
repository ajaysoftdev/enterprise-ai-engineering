# Enterprise Integration Platform

**Purpose:** Provide reusable, observable and resilient patterns for exchanging data and coordinating processes across enterprise applications.

**Domain:** Enterprise integration, API management, event-driven architecture and workflow orchestration.  
**Technology direction:** REST APIs, asynchronous messaging, canonical contracts and adapter-based connectors; specific broker/runtime choices will be documented as ADRs.  
**Status:** Reliability prototype CI verified — 6 tests passed on Python 3.12 (GitHub Actions run 42454847474, commit 1030523). This verifies local simulated delivery, retry, idempotency and DLQ tests only; it does not verify a production broker or exactly-once delivery.

## Business capabilities
- Expose and consume versioned APIs with consistent error contracts.
- Ingest and publish events with schema and compatibility controls.
- Support secure file-based integration where required.
- Map source payloads to canonical domain contracts.
- Route, transform and orchestrate multi-step exchanges.
- Handle retries, idempotency, dead-letter queues and replay.
- Trace transactions end to end across systems.

## Reference workflow
Source API/event/file → authentication and validation → canonical mapping → routing/orchestration → target adapter → acknowledgement/retry → dead-letter/replay → end-to-end monitoring.

## Key modules
- **API layer:** resource contracts, versioning and authentication.
- **Event layer:** event envelopes, schema registry concept and subscriptions.
- **Mapping:** canonical models, transformation and validation.
- **Orchestration:** workflow state, timeouts and compensation.
- **Reliability:** idempotency, retry policy, DLQ and replay.
- **Operations:** correlation IDs, metrics, tracing and operational dashboards.

## Expected demonstration
Integrate synthetic order, inventory and shipment services. Demonstrate synchronous API validation, asynchronous event propagation, duplicate message handling, failure routing and replay without duplicate business effects.

## Guardrails
Keep business rules out of transport adapters where possible. Version contracts deliberately, protect sensitive payloads, avoid logging secrets and define delivery guarantees explicitly.

## First executable slice

The current prototype includes a versioned event envelope, schema allow-list, idempotency-key handling, SQLite message persistence, bounded delivery retries, dead-letter routing, explicit replay and delivery audit events. It includes API tests, OpenAPI, a synthetic order event, Docker and a GitHub Actions workflow.

**Limitations:** delivery is simulated by an API call; there is no Kafka, Service Bus, RabbitMQ, API gateway, schema registry, external producer/consumer, distributed transaction, outbox relay, authentication, authorization, tenant isolation or production-grade broker semantics. Retry and DLQ state is local SQLite state, and replay is not concurrency-safe. Exactly-once delivery is not claimed. GitHub Actions executed the API suite successfully: 6 passed, 0 failed. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn integration.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml). Example event: [examples/order-created.json](examples/order-created.json).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No live middleware, production connector or throughput/SLA claim is made.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
