# Source-code layout — Predictive Life Sciences Supply Chain

```text
src/
  app/                  # composition, configuration, health
  api/                  # REST routes and request schemas
  contracts/
    api/                # OpenAPI specifications
    events/             # versioned event schemas
    canonical/          # canonical message models
  domain/
    entities.py         # Material, Lot, Batch, Shipment, InventoryPosition, PurchaseOrder, Study, Site, SupplyEvent, RiskPrediction, PlannerAction
    routing.py          # route and delivery invariants
    policies.py         # retry/idempotency/schema policies
  application/
    commands/           # publish, route, replay, reconcile
    ports.py             # broker, repository, endpoint contracts
  infrastructure/
    adapters/           # source_adapters, canonical_events, inventory, lot_traceability, feature_pipeline, forecasting, risk_scoring, planner_workbench, audit
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
