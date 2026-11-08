# Project 6: Enterprise Integration Architecture Case Study

- Status: Proposed
- Type: Fictional enterprise architecture design exercise

## Business scenario

A fictional distributor processes orders through a commerce channel, maintains customer and product information in core business systems, fulfils orders through a warehouse platform and sends shipment updates to customers. The systems have different data models and availability characteristics.

This scenario is intentionally fictional. It is not a description of a deployed customer environment.

## Architecture questions

- Which system owns each business entity and state transition?
- Which interactions require synchronous API responses?
- Which events can be processed asynchronously?
- How are duplicate messages, retries and out-of-order events handled?
- How are partial failures detected and reconciled?
- How are identities, authorization and sensitive fields protected?
- What should be monitored across service boundaries?

## Proposed logical flow

```text
Commerce channel
      |
      v
API gateway / integration boundary
      |
      +------> Order service ------> Order store
      |               |
      |               +---- Order accepted event
      |                            |
      v                            v
Customer / product lookup     Message broker
                                   |
                         +---------+---------+
                         v                   v
                    Warehouse          Notification
                    integration         service
                         |
                         v
                    Shipment event
                         |
                         v
                    Order status update
```

The diagram is a conceptual proposal. Specific technologies and deployment topology must be selected only after documenting requirements and constraints.

## Required architecture deliverables

1. Business capability and system-context view.
2. System inventory and data ownership matrix.
3. Order lifecycle and sequence diagrams.
4. API contracts and event schemas.
5. Error handling, retry, idempotency and reconciliation design.
6. Security and identity boundaries.
7. Observability and operational support model.
8. Deployment/environment view and non-functional requirements.
9. Architecture decision records with alternatives and trade-offs.

## Acceptance criteria

- Each system has a defined responsibility and data ownership boundary.
- Synchronous and asynchronous interactions have explicit reasons.
- Failure scenarios and recovery actions are documented.
- Event consumers are designed for duplicate delivery.
- Security, privacy and least-privilege requirements are addressed.
- Reliability, performance and support assumptions are measurable or marked as open questions.
- Diagrams and narrative agree with each other.
- Proposed choices are labelled as proposed, not implemented facts.

## Deliverables

Architecture pack, diagrams, interface examples, risk register, ADRs and a concise executive summary.
