# Local deployment and operations — Predictive Life Sciences Supply Chain

## Intended assets
- Dockerfile with pinned dependencies and non-root runtime.
- compose.yaml for app, database and local broker if required.
- .env.example with safe placeholders only.
- contracts/ for versioned API/event schemas.
- deploy/ for environment-neutral manifests.
- .github/workflows/ci.yml for lint, tests, contract checks and image build.

## Operations
Document queue depth, delivery latency, retry counts, dead-letter volume, consumer lag, reconciliation backlog, trace propagation and alert ownership. Define replay authorisation and operational runbooks.

## Status
Local deployment and CI execution are pending. No production integration or client connectivity is implied.
