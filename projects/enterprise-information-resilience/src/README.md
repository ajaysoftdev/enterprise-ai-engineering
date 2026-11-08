# Source-code layout — Enterprise Information Resilience

Intended implementation boundary:

```text
src/
  inforesilience/
    main.py              # signal intake, case correlation, human review and audit API
    models.py            # typed evidence, signal and review contracts
    scoring.py           # explainable synthetic risk and case aggregation
    repository.py        # SQLite signal, review and audit persistence
  app/
    main.py              # application composition/startup
    config.py            # typed environment configuration
    dependencies.py      # dependency wiring
    health.py            # liveness/readiness
  api/
    routes/              # versioned endpoints
    schemas/             # request/response contracts
    errors.py            # stable error envelope
  domain/
    entities.py          # Signal, Source, Claim, Entity, RiskAssessment, Case, ReviewDecision, ResponseAction, AuditEvent
    value_objects.py     # identifiers, statuses, invariants
    services.py          # pure domain rules
    events.py            # domain events
  application/
    commands/            # use-case handlers
    queries/             # read use cases
    ports.py              # repository and adapter interfaces
  infrastructure/
    persistence/         # repositories and migrations
    adapters/            # connectors, provenance, claim_extraction, entity_resolution, risk_scoring, case_management, human_review, response_workflow, audit
    messaging/           # publisher/consumer when needed
  observability/
    logging.py
    metrics.py
    tracing.py
```

## Implementation rules
- Domain code must import without starting the API server.
- Define ports in application and implementations in infrastructure.
- Replace external dependencies with deterministic fakes in unit tests.
- Use transactions for state changes and an outbox when DB/event consistency requires it.
- Make retryable commands idempotent.
- Fail fast on missing required configuration; redact secrets from logs.
- Keep provider SDKs and vendor-specific payloads inside adapters.

## First executable milestone
Add a build manifest and lock file, minimal application factory, liveness/readiness endpoints, one complete domain use case, one local persistence adapter and unit/API tests. This file is a design guide; source implementation and runtime verification are pending.
