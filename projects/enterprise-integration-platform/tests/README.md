# Test strategy — Enterprise Integration Platform

## Test layers
1. Unit: schema validation, mapping, routing and idempotency.
2. Application: orchestration with fake brokers and repositories.
3. Contract: OpenAPI/AsyncAPI compatibility and consumer contract tests.
4. Integration: broker/database transactions, retry and dead-letter handling.
5. End-to-end: synthetic multi-system flow: Producer → API/event/file ingress → schema and identity validation → routing/transformation → orchestration or choreography → retry/DLQ → consumer → trace/reconciliation.
6. Security: service identity, authorisation, secret handling and payload minimisation.
7. Resilience: duplicate, out-of-order, poison message, timeout, broker outage and replay.

## Synthetic fixtures
Generate Integration, Endpoint, Message, Schema, Mapping, Route, Subscription, DeliveryAttempt, DeadLetter, ReconciliationRecord fixtures with valid, malformed, duplicate, late and out-of-order examples. For the life-sciences project use synthetic lot, shipment, inventory and study records only.

## Definition of done
Schemas validate; transformations have positive/negative tests; delivery is idempotent; retry/DLQ/replay are tested; end-to-end run is reproducible; CI retains evidence. Do not claim delivery guarantees without tests.

## Current executable test slice
The current API suite covers health, idempotent message publication, successful delivery, retry exhaustion, dead-letter replay, invalid event-type rejection and delivery audit. It does not exercise a real broker, cross-system exactly-once semantics, concurrent consumers, schema-registry compatibility, authentication or distributed tracing.

## Evidence
Record commit, tool versions, commands, test counts, results and exclusions. Untested checks remain planned.
