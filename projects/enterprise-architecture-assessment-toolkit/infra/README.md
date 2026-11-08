# Local deployment and operations — Enterprise Architecture Assessment Toolkit

## Intended assets
- Dockerfile and compose.yaml for local application and database.
- .env.example with safe dummy settings.
- schemas/ for versioned SAP-like and canonical contracts.
- migrations/ for persistence changes.
- deploy/ for future environment templates.
- .github/workflows/ci.yml for lint, tests and schema checks.

## Operations
Track batch status, source/target counts, rejected records, reconciliation variance, CDC lag, retries, load duration and lineage completeness. Document restart, replay and rollback procedures.

## Status
A synthetic local simulator is the initial target. Live SAP connection, cloud deployment and production migration are not implied.
