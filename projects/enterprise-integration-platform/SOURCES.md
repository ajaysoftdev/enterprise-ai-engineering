# Reference sources — Enterprise Integration Platform

## API and event contracts
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — REST API contract definition.
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest) — asynchronous API and message-driven contracts.
- [CloudEvents](https://cloudevents.io/) — portable event metadata envelope.
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — distributed event streaming concepts and operational configuration.
- [OAuth 2.0 Security Best Current Practice (RFC 9700)](https://www.rfc-editor.org/rfc/rfc9700) — modern OAuth security guidance.

## Architecture and operations
- [SAP Integration Architecture Guide](https://help.sap.com/docs/sap-btp-guidance-framework/integration-architecture-guide) — integration styles and hybrid integration methodology.
- [OpenTelemetry](https://opentelemetry.io/docs/) — distributed tracing and observability.
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — message routing, transformation and endpoint patterns.

## Apply these references to this project
Select synchronous APIs, asynchronous events, batch/file exchange or orchestration according to business coupling and delivery requirements. Specify schema evolution, idempotency, ordering, retries, DLQ, replay, security and reconciliation for each integration. Do not assume exactly-once delivery across independent systems.
