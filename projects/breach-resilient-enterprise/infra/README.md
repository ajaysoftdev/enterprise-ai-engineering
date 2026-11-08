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

## Current local assets
A Dockerfile, Docker Compose service and GitHub Actions test workflow are now present. The container runs the FastAPI demonstrator as a non-root user.

## Status
No production deployment is implied. CI execution and operational verification remain pending. The service is a synthetic simulation and has no connection to enterprise identity, cloud or network controls.
