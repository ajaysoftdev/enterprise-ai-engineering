# Predictive Life Sciences Supply Chain

**Purpose:** Improve visibility of material availability, lot status and delivery risk across regulated life-sciences supply chains.

**Domain:** Life-sciences operations, supply chain analytics and predictive risk.  
**Technology direction:** Domain APIs, event ingestion, governed analytical data and explainable risk models; implementation choices will be recorded as ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

## Business capabilities
- Represent materials, suppliers, purchase orders, inventory, lots and shipments.
- Ingest ERP, WMS, manufacturing, quality and logistics events.
- Track lot genealogy, expiry, quality holds and release status.
- Identify shortages, delays and material constraints.
- Calculate explainable risk indicators and scenario impacts.
- Present planner work queues and recommended next actions.

## Reference workflow
Operational source events → canonical supply-chain model → lot and order reconciliation → availability calculation → risk feature generation → prediction/scenario analysis → planner review → action and outcome capture.

## Key modules
- **Domain model:** material, supplier, order, lot, shipment and site.
- **Ingestion:** synthetic ERP/WMS/MES/QMS and logistics adapters.
- **Traceability:** lot genealogy, status and event history.
- **Planning:** demand/supply balance, constraints and exception queues.
- **Risk analytics:** delay/shortage features and explainable risk scoring.
- **Planner workflow:** review, action assignment and outcome feedback.

## Expected demonstration
Use synthetic pharmaceutical supply data to identify a lot on quality hold that affects a planned production order, calculate downstream shortage exposure and route the issue to a planner.

## Guardrails
Preserve lot-level traceability and data provenance. Predictions support planning decisions; they do not release batches, change quality status or replace authorised quality processes.

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
Use synthetic data and clearly labelled simulated events. No validated GxP system, regulated production use or forecast accuracy is claimed.