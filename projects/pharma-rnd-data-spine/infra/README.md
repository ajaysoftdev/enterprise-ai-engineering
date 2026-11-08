# Local deployment and operations — Pharma R&D Data Spine

## Intended assets
- Dockerfile and compose.yaml for local reproducible execution.
- .env.example containing safe placeholders.
- schemas/ and migrations/ for versioned contracts and metadata storage.
- deploy/ for environment-specific infrastructure templates.
- .github/workflows/ci.yml for lint, tests, schema checks and build.

## Operations
Track pipeline duration, freshness, records read/written/quarantined, quality failures, retries, checkpoint age, lineage completeness and estimated compute/storage cost. Document replay and backfill controls.

## Status
Cloud account provisioning, cloud deployment and runtime verification are pending. No cloud execution is implied by this specification.
