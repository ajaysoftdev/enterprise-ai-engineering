# Source-code layout — Third-Party Risk Management

```text
src/
  app/                  # config, composition and health
  api/
    routes/             # versioned endpoints
    schemas/            # task/evidence contracts
  domain/
    entities.py         # Vendor, Service, RiskTier, Assessment, Control, Evidence, Finding, Approval, AccessGrant, FourthParty, ReviewEvent
    policies.py         # invariants and permissions
    state_machine.py    # valid lifecycle transitions
  application/
    commands/           # submit, execute, approve, assess, report
    ports.py             # agent/Git/sandbox/vendor-system interfaces
  infrastructure/
    adapters/           # vendor_registry, intake, tiering, questionnaire, evidence, control_assessment, approvals, access_review, monitoring, offboarding
    persistence/        # repositories and migrations
    sandbox/            # isolated execution implementation
  evaluation/           # test harness, scoring and evidence
  observability/        # logs, metrics and traces
```

## Engineering rules
- No untrusted code execution outside an isolated sandbox.
- Enforce tool allowlists, timeouts, token/cost budgets and cancellation.
- Preserve original inputs, diffs, logs and test evidence.
- Make scoring explainable and version evaluation rubrics.
- Do not treat a model assertion as proof of a test result.
- Keep secrets out of prompts, logs and artifacts.

## First executable milestone
Implement one deterministic task, a fake agent adapter, isolated temporary workspace, command runner, result schema and tests. Live model/provider execution is a later adapter.
