# Project Blueprint — Enterprise Portfolio Integration

## Business objective
Demonstrate how independently owned enterprise capabilities can collaborate through stable contracts without sharing databases or bypassing domain governance.

## Initial scenario
A supplier invoice enters the portfolio. Document Intelligence extracts invoice and supplier attributes. MDM creates a supplier source record or flags a possible duplicate. The integration workflow tracks the process and waits for human stewardship where needed.

## Scope
- Supplier invoice onboarding.
- Document extraction adapter.
- MDM source-record adapter.
- Idempotent workflow orchestration.
- Human stewardship pause and refresh.
- Audit and error-state visibility.

## Out of scope
- Live ERP, SAP, CRM or procurement connectors.
- Event broker, API gateway, schema registry or service mesh.
- Automatic MDM merge or supplier approval.
- OCR, PDF/image parsing, LLM extraction or real supplier validation.
- Production authentication, authorization, tenant isolation or cloud deployment.

## Demonstration
Start Document Intelligence, MDM and Integration services locally. Submit a synthetic invoice with supplier name, tax identifier, invoice number and total. Inspect the workflow, MDM record and audit trail. Submit a second invoice with the same tax ID and demonstrate the steward-pending state. Approve/reject through the MDM API, then refresh the integration workflow.

## Definition of done
Automated API tests, Docker build, explicit state machine, idempotency conflict tests, adapter failure tests, OpenAPI contract and clear limitations.
