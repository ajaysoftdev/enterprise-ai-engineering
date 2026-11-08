# Local deployment and operations — Third-Party Risk Management

## Intended assets
- Dockerfile and compose.yaml for local API and state store.
- .env.example with safe placeholders only.
- sandbox/ for isolated runtime configuration.
- migrations/ for versioned storage changes.
- .github/workflows/ci.yml for lint, tests and build.

## Operations
Track task/run state, execution duration, tool calls, budget consumption, sandbox failures, policy denials, test outcomes and evidence retention. Define artifact expiry and secure cleanup.

## Status
No live agent execution or vendor-system connection is implied. Local sandbox, CI and runtime verification remain pending.
