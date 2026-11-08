# Reference sources — SAP S/4HANA Data Modernisation

## SAP architecture and migration
- [SAP Integration Architecture Guide](https://help.sap.com/docs/sap-btp-guidance-framework/integration-architecture-guide) — integration styles and hybrid SAP landscapes.
- [SAP S/4HANA Migration Cockpit](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE) — SAP migration documentation entry point; select the target release and deployment model.
- [SAP Architecture Center](https://architecture.learning.sap.com/) — SAP reference architectures for data, integration, security and AI.
- [SAP Big Picture Architecture](https://www.sap.com/documents/sap-big-picture-architecture-1183374) — BTP, data, integration and S/4HANA transformation context.
- [SAP Document Processing Reference Architecture](https://architecture.learning.sap.com/docs/ref-arch/744df4) — example of SAP document-to-business-system integration.

## Data contracts and governance
- [OpenAPI](https://spec.openapis.org/oas/latest.html) — API contracts for source and target adapters.
- [CloudEvents](https://cloudevents.io/) — event envelope for change-data events.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) — mapping and migration lineage.
- [OpenLineage](https://openlineage.io/docs/) — pipeline lineage.

## Apply these references to this project
Use synthetic SAP-like records and clearly label all interfaces as simulated unless connected to an SAP sandbox. Separate initial migration from delta/CDC, preserve source keys, make loads restartable and reconcile counts plus key attributes. Confirm release-specific SAP behaviour against the customer’s target system documentation.
