# Source-code layout — Enterprise MDM and Data Governance

```text
src/
  app/                  # application factory, config, dependency wiring, health
  api/
    routes/             # versioned HTTP endpoints
    schemas/            # typed request/response models
    errors.py            # stable error envelope
  domain/
    entities.py         # SourceSystem, Party, Supplier, Customer, Product, Location, MatchCandidate, GoldenRecord, StewardshipCase, DataQualityResult
    value_objects.py    # identifiers, states and invariants
    services.py         # pure business rules
    events.py           # domain events
  application/
    commands/           # use-case handlers
    queries/            # read use cases
    ports.py             # repository and external adapter contracts
  infrastructure/
    persistence/        # repositories and migrations
    adapters/           # connectors, canonical_model, standardization, matching, survivorship, stewardship, golden_record, distribution, lineage, quality
    messaging/          # optional publisher/consumer
  observability/        # logs, metrics and tracing
```

## Code design requirements
- Domain code must import without starting the API.
- Controllers validate/translate input and delegate to application services.
- External systems are accessed only through adapters.
- Use deterministic fakes in unit tests.
- Make retryable commands idempotent; use bounded retries.
- Use transactions and an outbox where database/event consistency requires it.
- Validate configuration at startup; redact credentials and sensitive values.

## First executable milestone
Create a build manifest and lock file, minimal app factory, liveness/readiness endpoints, one complete use case, local persistence adapter and unit/API tests. This describes the intended code; implementation remains pending.
