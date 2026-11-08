# High-Level Design: Enterprise Integration Case Study

- Status: Proposed
- Scope: Fictional order-to-fulfilment scenario
- Related project: [Project brief](../../projects/enterprise-integration-architecture/README.md)

## 1. Business context
A fictional distributor receives digital orders, validates customer and product information, coordinates warehouse fulfilment, publishes shipment status and triggers invoicing. This is an architecture exercise, not a deployed customer solution.

## 2. Capabilities and candidate systems

| Capability | Outcome | Candidate system |
|---|---|---|
| Digital commerce | Capture orders | Commerce channel |
| Customer/product master | Maintain trusted records | ERP or MDM |
| Order management | Coordinate order lifecycle | Order service |
| Fulfilment | Pick, pack and dispatch | WMS |
| Shipment visibility | Publish delivery status | Carrier adapter |
| Finance | Invoice and reconcile | ERP / finance |

Ownership is a proposed starting point and must be validated with business stakeholders.

## 3. Context view

    Customer -> Commerce channel -> API / integration boundary
                                      |
                     +----------------+----------------+
                     |                |                |
                 Order service      ERP / MDM        WMS adapter
                     |                                 ^
                     v                                 |
                 Event broker -------------------------+
                     |
                Notification
                     |
                  Customer

## 4. Component responsibilities

| Component | Responsibility | Boundary |
|---|---|---|
| API gateway | Identity, quotas, routing, request policy | No business orchestration |
| Order service | Validate and coordinate order state | Owns order lifecycle only if agreed |
| ERP adapter | Translate ERP-specific contracts | Isolates vendor details |
| WMS adapter | Translate fulfilment commands/events | Idempotent processing |
| Broker | Buffer and distribute events | Assume at-least-once delivery |
| Notification | Send approved status updates | Does not own order truth |
| Observability | Correlate and monitor flows | Redact sensitive payloads |

## 5. Integration patterns
- Synchronous APIs for immediate validation and acknowledgement.
- Asynchronous events for fulfilment and notifications.
- Transactional outbox where state change and event publication must remain consistent.
- Idempotency keys for retried commands.
- Bounded retries, dead-letter handling and controlled replay.
- Reconciliation for ambiguous or long-running outcomes.

## 6. Quality attributes

| Attribute | Questions / evidence |
|---|---|
| Availability | Business availability target and dependency map |
| Performance | Peak rates, latency budgets and workload tests |
| Reliability | Duplicate, retry and partial-failure tests |
| Security | Identity, data classification and threat model |
| Scalability | Independent scaling and capacity model |
| Operability | Dashboards, alerts and stuck-order runbooks |
| Recoverability | Agreed RTO/RPO and restore exercises |

## 7. Deployment
No cloud topology is selected. Compare managed integration services, containers and existing enterprise middleware against skills, cost, latency, security and operational constraints.

## 8. Open questions
- Which platform owns authoritative order status?
- Can ERP accept idempotency references?
- What ordering guarantees exist for WMS events?
- How are stuck orders reconciled?
- Which fields are personal or commercially sensitive?
- What are the volumes, SLAs, RTO and RPO?

## 9. Acceptance
System boundaries, data ownership, API/event distinctions, failure recovery, security and operations must be documented. Proposed elements must not be represented as deployed facts.
