# Test strategy — Predictive Life Sciences Supply Chain

## Test layers
1. Unit: schema validation, mapping, routing and idempotency.
2. Application: orchestration with fake brokers and repositories.
3. Contract: OpenAPI/AsyncAPI compatibility and consumer contract tests.
4. Integration: broker/database transactions, retry and dead-letter handling.
5. End-to-end: synthetic multi-system flow: Source events → canonical supply events → quality/lineage checks → inventory and lead-time features → risk prediction → planner review → action tracking.
6. Security: service identity, authorisation, secret handling and payload minimisation.
7. Resilience: duplicate, out-of-order, poison message, timeout, broker outage and replay.

## Synthetic fixtures
Generate Material, Lot, Batch, Shipment, InventoryPosition, PurchaseOrder, Study, Site, SupplyEvent, RiskPrediction, PlannerAction fixtures with valid, malformed, duplicate, late and out-of-order examples. For the life-sciences project use synthetic lot, shipment, inventory and study records only.

## Definition of done
Schemas validate; transformations have positive/negative tests; delivery is idempotent; retry/DLQ/replay are tested; end-to-end run is reproducible; CI retains evidence. Do not claim delivery guarantees without tests.

## Evidence
Record commit, tool versions, commands, test counts, results and exclusions. Untested checks remain planned.
