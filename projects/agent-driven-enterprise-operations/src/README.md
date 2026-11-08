# Source-code layout — Agent-Driven Enterprise Operations

```text
src/
  agentops/
    main.py              # workflow API and human decision endpoints
    models.py            # typed workflow and approval contracts
    policy.py            # fixed allow-list, risk classification and plan selection
    repository.py        # SQLite workflow and audit persistence
  app/                  # application factory, config, dependency wiring, health
  api/
    routes/             # versioned HTTP endpoints
    schemas/            # typed request/response models
    errors.py            # stable error envelope
  domain/
    entities.py         # Workflow, AgentRun, Plan, Tool, ToolPermission, PolicyDecision, ApprovalRequest, Task, Exception, RunEvidence
    value_objects.py    # identifiers, states and invariants
    services.py         # pure business rules
    events.py           # domain events
  application/
    commands/           # use-case handlers
    queries/            # read use cases
    ports.py             # repository and external adapter contracts
  infrastructure/
    persistence/        # repositories and migrations
    adapters/           # agent_runtime, planner, tool_registry, policy_guard, workflow_state, approval, exception_handling, memory_adapter, telemetry, audit
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
