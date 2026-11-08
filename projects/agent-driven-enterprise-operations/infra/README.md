# Local deployment and operations — Agent-Driven Enterprise Operations

## Intended assets
- Dockerfile: pinned dependencies, minimal image and non-root runtime.
- compose.yaml: local application and required dependencies.
- .env.example: documented settings with safe dummy values only.
- migrations/: versioned schema changes.
- deploy/: environment-neutral deployment templates.
- .github/workflows/ci.yml: lint, type-check, tests and image build.

## Configuration
Keep environment-specific values outside source control. Validate required settings at startup and redact secrets from logs.

## Operations
Document health/readiness, structured logs, metrics, traces, backup/restore, migration rollback, dependency outage and incident escalation as implemented.

## Status
No production deployment is implied. Containerisation, CI execution and operational verification remain pending.
