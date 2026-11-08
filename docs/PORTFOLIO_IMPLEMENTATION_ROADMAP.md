# Enterprise AI Engineering Portfolio — Implementation Roadmap

## Portfolio delivery objective

Turn the 15 documented project concepts into a coherent, demonstrable portfolio of enterprise architecture and engineering solutions. Each project must have a runnable local profile, synthetic sample data, automated tests, security controls, operational visibility and clear evidence of what is implemented versus simulated.

## Delivery gates (apply to every project)

| Gate | Required evidence | Exit condition |
|---|---|---|
| G0 — Architecture | Project brief, sources, logical architecture, boundaries, workflow, proposed contracts, domain concepts, risks | Scope and assumptions are explicit |
| G1 — Foundation | Runtime configuration, dependency lock/constraints, health endpoint, structured logging, migrations, CI | Clean local startup |
| G2 — Domain | Domain entities, validation, state transitions, repository layer, deterministic rules | Unit tests pass |
| G3 — Workflow | Primary business process, API/event contracts, synthetic fixtures, idempotency and failure handling | End-to-end demo passes |
| G4 — Trust | Authentication/authorization design, audit, secret handling, input validation, threat tests | Security tests pass |
| G5 — Operations | Metrics, traces, health/readiness, retry/replay, backup/restore and runbook | Operational walkthrough complete |
| G6 — Packaging | Docker/local profile, seed data, API docs, screenshots or sample output, CI evidence | Reproducible demonstration |
| G7 — Review | Architecture decisions, limitations, known gaps, performance test evidence | No unsupported production/compliance claims |

A project is not marked Verified until the required tests have actually run and their results are recorded. A specification or successful GitHub commit is not implementation verification.

## Recommended implementation sequence

The sequence groups projects by reusable foundations and business dependencies. It is a delivery order, not a statement that later projects are less important.

| Order | Project | Main reusable capability |
|---:|---|---|
| 1 | Enterprise Document Intelligence | API, validation, evidence, review workflow, persistence |
| 2 | Enterprise MDM and Data Governance | Canonical entities, matching, stewardship, lineage |
| 3 | Enterprise Integration Platform | API/event contracts, idempotency, retry, DLQ, reconciliation |
| 4 | Cloud Data Engineering Platform | Ingestion, orchestration, quality, lineage, lakehouse |
| 5 | Enterprise Data Protection | Classification, policy decisions, masking, audit |
| 6 | Agent-Driven Enterprise Operations | Durable workflows, bounded agents, tool policy, approval |
| 7 | Autonomous AI Engineering Workbench | Sandboxing, repository tools, evaluation and CI |
| 8 | Enterprise Architecture Assessment Toolkit | Capability model, inventory, evidence, options and roadmap |
| 9 | Breach-Resilient Enterprise | Identity/asset graph, detection, containment simulation |
| 10 | Enterprise Attention Intelligence Hub | Telemetry, topology, correlation, SLOs and work queues |
| 11 | Third-Party Risk Management | Evidence, control mapping, risk and remediation |
| 12 | SAP S/4HANA Data Modernisation | Migration framework, mapping, delta and reconciliation |
| 13 | Pharma R&D Data Spine | Scientific metadata, sample identity and lineage |
| 14 | Predictive Life Sciences Supply Chain | Event traceability, features, prediction and planner feedback |
| 15 | Enterprise Information Resilience | Source evidence, claims, assessments and response governance |
| 16 | Enterprise Portfolio Integration | Cross-project adapters, idempotent orchestration, stewardship handoff and end-to-end traceability |

## Shared engineering standards

- Prefer modular monoliths initially; introduce services only for independently justified scaling, ownership or isolation.
- Keep business/domain rules provider-neutral and isolate vendor services behind adapters.
- Use OpenAPI for synchronous APIs and AsyncAPI/CloudEvents where asynchronous contracts are needed.
- Use stable IDs, UTC timestamps, correlation IDs, idempotency keys, schema versions and explicit error contracts.
- Treat external text, documents, events and repository content as untrusted input.
- Keep AI-generated content advisory; deterministic validation, authorization and human approval govern consequential actions.
- Use synthetic data in public repositories. Never commit credentials, private keys, customer data or production exports.
- Add unit, contract, integration, security and end-to-end tests. Capture actual test results in CI.
- Publish architecture decisions as ADRs and update status only when evidence exists.
- Distinguish proposed architecture, implemented code, locally tested behaviour, CI-verified behaviour and production operation.

## Cross-project platform capabilities

Build once and reuse where sensible:
1. Identity and authorization contracts.
2. Audit event envelope and correlation identifiers.
3. API error and pagination conventions.
4. Configuration and secret-provider abstraction.
5. Health, metrics, logs and traces.
6. Test fixtures and synthetic data generation.
7. Container build and CI workflow.
8. Data lineage and evidence reference conventions.
9. Human approval workflow for high-impact actions.
10. Shared policy and risk decision patterns.

Avoid creating a central framework prematurely. Extract shared libraries only after two or more projects demonstrate a stable common requirement.

## Current status

- The 15 core domain projects retain their project-specific scope, reference sources, implementation architecture, domain contracts and delivery guidance; the sixteenth portfolio integration project now has its own architecture and first vertical slice.
- All 16 projects now have a first executable local prototype slice, API contracts, Docker configuration, automated tests and project-specific GitHub Actions workflows.
- All 16 current-revision GitHub Actions test workflows completed successfully on Python 3.12: **119 tests passed across the portfolio**.
- All 16 Docker images built successfully in their respective CI workflows.
- This evidence verifies the current synthetic/local prototype slices only. It does not establish production readiness, live enterprise integration, security certification, GxP validation, cloud deployment, performance or regulatory compliance.
- Every project README records its own CI run, test count and explicit limitations.
- The Starlette TestClient deprecation warning was resolved by adding `httpx2` to the development dependencies; the latest CI reruns complete without that warning.
- Portfolio Bandit and `pip-audit --skip-editable` scans passed for the 15 core projects in GitHub Actions run 42461092337 after upgrading pytest to 9.0.3. The integration project's security scan is pending. See [Portfolio Security Baseline](PORTFOLIO_SECURITY_BASELINE.md).
- Request correlation middleware, bounded caller-provided IDs, generated fallback IDs and baseline response headers have been added across all 15 core APIs; the new regression tests passed in the current CI runs.
- MDM stewardship decisions now use a single SQLite transaction for candidate state, decision record and golden-record update; a regression test covers duplicate decisions without partial mutation and passed in CI.
- The sixteenth project's first vertical slice connects Document Intelligence to MDM through an idempotent supplier-onboarding workflow. Its 10-test suite, Docker build and three-service HTTP smoke test passed; the workflow verified Document Intelligence → MDM → Integration, including a steward decision and refresh.
- Next engineering milestone: resolve security-scan findings, add authentication/authorization and tenant-isolation controls, test concurrent requests and recovery, and add operational telemetry and reproducible deployment verification. Expand the sixteenth integration project only as each domain interface and control becomes sufficiently stable.

## Current official architecture references

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — AI risk governance; NIST notes the framework is under revision.
- [NIST SP 800-228 update](https://csrc.nist.gov/pubs/sp/800/228/upd1/final) — API protection guidance, including lifecycle risk and controls.
- [ISO/IEC/IEEE 42030:2019](https://www.iso.org/standard/73436.html) — architecture evaluation framework; ISO confirms the 2019 edition remains current while a second edition is under development.
- [Australian Government AI Reference Architecture](https://www.digital.gov.au/ai-reference-architecture) — architecture, assurance and human oversight reference.

