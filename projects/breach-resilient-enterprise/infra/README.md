# Local deployment and operations — Breach-Resilient Enterprise

## Intended assets
- Dockerfile: minimal runtime image, pinned dependencies, non-root execution.
- compose.yaml: application and required local dependencies.
- .env.example: documented variable names and safe dummy values only.
- migrations/: versioned database schema changes.
- deploy/: environment-neutral deployment templates.
- .github/workflows/ci.yml: lint, type-check, unit/integration tests and image build.

## Configuration
Keep environment-specific values outside source control. Separate development, test and production settings. Validate required variables at startup and redact secrets from logs.

## Operations
Expose liveness/readiness, structured logs, metrics and trace context. Document backup/restore, migration rollback, dependency outage, queue/DLQ inspection and incident escalation as capabilities are implemented.

## Status
No production deployment is implied. Local containerisation, CI execution and operational verification remain pending implementation.
