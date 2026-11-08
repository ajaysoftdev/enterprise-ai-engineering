# Architecture

This area records application structure, design reasoning and technical decisions for the portfolio exercises.

## Integrated enterprise reference model

The portfolio-level target-state architecture connects business capabilities and operating model with enterprise data, integration, AI, security, observability, resilience and engineering delivery.

- [Integrated enterprise reference architecture](../docs/architecture/enterprise-reference-architecture.md)
- [Enterprise capability map](../docs/architecture/capability-map.md)
- [Portfolio module dependency map](../docs/architecture/module-dependency-map.md)

## Featured project

[Enterprise integration architecture case study](../projects/enterprise-integration-architecture/README.md)

A proposed architecture case study for a fictional order-processing environment. It explores system context, API and event boundaries, data ownership, failure handling, security, observability, deployment and architecture decision records. It is a design exercise, not a claim about a deployed customer system.

## Documentation scope

- System context and major components
- Key application and request flows
- Data model and persistence boundaries
- API and integration boundaries
- Synchronous APIs versus asynchronous events
- Retry, idempotency, dead-letter and reconciliation patterns
- Configuration and deployment assumptions
- Quality attributes such as security, reliability and performance
- Architecture decisions and trade-offs

## Architecture decision records

Use the [ADR template](decision-record-template.md) for decisions that materially affect structure, dependencies or long-term maintainability.

Architecture descriptions must reflect code and evidence actually inspected. Mark inferred or proposed designs clearly; do not present them as implemented facts.

## Status

Architecture documentation structure and case-study specification prepared. No production deployment or customer implementation is claimed.
