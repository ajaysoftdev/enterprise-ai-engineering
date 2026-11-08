# Low-Level Design: Integration Case Study

- Status: Proposed
- Parent: [HLD](HLD.md)

## 1. Scope
Define illustrative contracts and runtime behaviour for the fictional order scenario. These are not implemented APIs.

## 2. Order intake example

    {
      "externalOrderId": "WEB-100045",
      "customerReference": "CUST-204",
      "currency": "INR",
      "items": [{"sku": "SKU-100", "quantity": 2}],
      "idempotencyKey": "WEB-100045-v1"
    }

Validate unique external ID within source scope, supported currency, non-empty items, positive integer quantity, resolvable references and deterministic duplicate handling.

## 3. Proposed order states

    Received -> Validating -> Rejected
                         -> Accepted -> ReleasedToWarehouse
                                      -> PartiallyFulfilled
                                      -> Fulfilled -> Closed
    Accepted / ReleasedToWarehouse -> CancelRequested
    CancelRequested -> Cancelled or Rejected

Confirm partial shipment and cancellation rules with business owners.

## 4. Event envelope example

    {
      "eventId": "evt-00001",
      "eventType": "ShipmentDispatched",
      "eventVersion": 1,
      "occurredAt": "2026-01-01T10:00:00Z",
      "correlationId": "WEB-100045",
      "aggregateId": "ORD-90001",
      "source": "warehouse-adapter",
      "data": {"shipmentReference": "SHP-3001"}
    }

Consumers validate schema version, deduplicate event identity and persist processing outcome.

## 5. Failure matrix

| Failure | Handling |
|---|---|
| Invalid request | Reject with field-level reason |
| Duplicate command | Return prior outcome or defined conflict |
| ERP timeout | Retry only when safe; otherwise mark outcome unknown |
| WMS unavailable | Persist pending command and retry asynchronously |
| Invalid event | Quarantine and alert |
| Duplicate event | Acknowledge without repeating side effects |
| Out-of-order event | Check aggregate state/version and reconcile |
| Poison message | Dead-letter after bounded attempts |

## 6. Security and observability
Use service identities, TLS, least privilege, payload validation, size limits, redaction and audit for replay. Correlate event ID, order surrogate, source, destination, attempt, outcome and duration. Never log credentials or sensitive payloads.

## 7. Required tests
Contract validation, idempotent command replay, duplicate/out-of-order events, retry exhaustion, dead-letter routing, timeout recovery and reconciliation.

## 8. Open decisions
Database, broker, gateway, delivery guarantee, ordering key, schema registry and deployment platform remain undecided pending requirements.
