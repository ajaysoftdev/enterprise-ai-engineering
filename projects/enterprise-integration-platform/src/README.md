# Source-code layout — Enterprise Integration Platform

```text
src/
  integration/
    main.py              # message intake, delivery, retry, DLQ and replay endpoints
    models.py            # versioned event and process contracts
    repository.py        # SQLite message, deduplication and audit persistence
  app/                  # composition, configuration, health
  api/                  # REST routes and request schemas
  contracts/
    api/                # OpenAPI specifications
    events/             # versioned event schemas
    canonical/          # canonical message models
  domain/
    entities.py         # Integration, Endpoint, Message, Schema, Mapping, Route, Subscription, DeliveryAttempt, DeadLetter, ReconciliationRecord
    routing.py          # route and delivery invariants
    policies.py         # retry/idempotency/schema policies
  application/
    commands/           # publish, route, replay, reconcile
    ports.py             # broker, repository, endpoint contracts
  infrastructure/
    adapters/           # api_gateway_adapter, event_bus_adapter, file_gateway, schema_registry, canonical_mapping, routing, orchestration, retry, dead_letter, observability
    persistence/        # delivery state and migrations
    messaging/          # broker implementation
  observability/        # trace propagation, metrics, logs
```

## Engineering rules
- Keep canonical schemas independent of transport.
- Never assume exactly-once delivery; design idempotent consumers.
- Bound retries and route exhausted messages to a dead-letter workflow.
- Preserve correlation and causation IDs across hops.
- Make replay explicit, authorised and auditable.
- Test schema compatibility and transformation edge cases.

## First executable milestone
Implement a canonical message envelope, one in-memory broker adapter, one route, one idempotent consumer and tests for duplicate delivery and invalid schema. Runtime implementation remains pending.
