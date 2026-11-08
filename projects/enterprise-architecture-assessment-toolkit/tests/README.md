# Test strategy — Enterprise Architecture Assessment Toolkit

## Test layers
1. Unit: mapping, canonicalisation, validation and survivorship rules.
2. Contract: SAP-facing and canonical schema validation.
3. Integration: persistence, batch state, target adapter and CDC adapter.
4. Migration: initial load, delta load, replay and reconciliation.
5. End-to-end: synthetic scenario covering Assessment intake → capability map → stakeholder evidence → current-state inventory → dependency/gap analysis → target options → roadmap/decisions.
6. Security: credentials, access boundary, sensitive-field masking and audit.
7. Resilience: duplicate change event, malformed row, partial batch, target outage and restart.

## Synthetic fixtures
Create Assessment, BusinessDriver, Capability, Process, InformationObject, Application, TechnologyComponent, Dependency, Gap, Option, RoadmapInitiative, Decision records with duplicates, missing required values, invalid references, changed attributes and late changes. Never use real business partner/customer records.

## Definition of done
Mapping is deterministic; invalid records are quarantined; loads are idempotent; source/target reconciliation is repeatable; lineage identifies mapping version; CI retains reports.

## Evidence
Record commit, fixture version, command, source/target counts, rejected rows, reconciliation results and test counts. Untested checks remain planned.
