# Project Catalogue

This directory contains fifteen independently scoped core enterprise workstreams, one portfolio integration project, plus six earlier engineering exercises. All sixteen portfolio projects each have a project overview, detailed blueprint, curated reference sources, implementation architecture, domain contracts/data model and delivery/test guidance.

The project folders are maintained inside this repository; they are not separate GitHub repositories.

## Sixteen enterprise portfolio projects

| # | Project | Primary business capability | Status |
|---:|---|---|---|
| 1 | [Enterprise Information Resilience](enterprise-information-resilience/README.md) | Digital trust, information integrity and reputation resilience | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478814374) |
| 2 | [Enterprise Document Intelligence](enterprise-document-intelligence/README.md) | Document extraction, validation and human exception handling | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478818147) |
| 3 | [Breach-Resilient Enterprise](breach-resilient-enterprise/README.md) | Zero-trust architecture and attack-path containment | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478821593) |
| 4 | [Enterprise Data Protection](enterprise-data-protection/README.md) | Data classification, minimisation, masking and access governance | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478825871) |
| 5 | [Enterprise Attention and Intelligence Hub](enterprise-attention-intelligence-hub/README.md) | Business-impact observability and decision prioritisation | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478830047) |
| 6 | [Enterprise MDM and Data Governance](enterprise-mdm-data-governance/README.md) | Matching, survivorship, stewardship and golden records | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478842872) |
| 7 | [Agent-Driven Enterprise Operations](agent-driven-enterprise-operations/README.md) | Bounded agents, policy checks and human approvals | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478847750) |
| 8 | [Enterprise Integration Platform](enterprise-integration-platform/README.md) | APIs, events, routing, orchestration and reliability | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478852405) |
| 9 | [Predictive Life Sciences Supply Chain](predictive-life-sciences-supply-chain/README.md) | Supply visibility, lot traceability and risk prediction | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478856948) |
| 10 | [Pharma R&D Data Spine](pharma-rnd-data-spine/README.md) | Research data harmonisation, traceability and lineage | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478860840) |
| 11 | [Cloud Data Engineering Platform](cloud-data-engineering-platform/README.md) | Ingestion, lakehouse transformations, quality and FinOps | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478872883) |
| 12 | [Autonomous AI Engineering Workbench](autonomous-ai-engineering-workbench/README.md) | Sandboxed coding-agent evaluation and evidence reporting | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478877471) |
| 13 | [Third-Party Risk Management](third-party-risk-management/README.md) | Vendor lifecycle, due diligence and fourth-party risk | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478881646) |
| 14 | [SAP S/4HANA Data Modernisation](sap-s4-data-modernisation/README.md) | SAP-like master data migration and reconciliation | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478886356) |
| 15 | [Enterprise Architecture Assessment Toolkit](enterprise-architecture-assessment-toolkit/README.md) | Capability-led assessment and target-state roadmapping | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478891292) |
| 16 | [Enterprise Portfolio Integration](enterprise-portfolio-integration/README.md) | Cross-project orchestration and contract-based workflows | CI + Docker + authenticated HTTP E2E + security verified — 13 tests passed (GitHub Actions run 42478896221) |

## Earlier engineering exercises

1. [Spring PetClinic service enhancement](java-spring-petclinic/README.md) — Java, Spring Boot, REST, persistence and regression testing.
2. [Python batch data pipeline](python-batch-data-pipeline/README.md) — ingestion, transformation, validation and batch reliability.
3. [Data quality framework](data-quality-framework/README.md) — reusable data contracts, profiling, validation and quality reporting.
4. [AI agent evaluation workbench](ai-agent-evaluation-workbench/README.md) — reproducible coding-agent tasks, diff review and evaluation reports.
5. [Quality automation pipeline](quality-automation-pipeline/README.md) — automated test and quality gates in CI.
6. [Enterprise integration architecture case study](enterprise-integration-architecture/README.md) — system context, APIs, events, resilience, security and ADRs.

## Status definitions

- **Specified:** business scope, architecture and implementation guidance are documented; executable implementation and verification are not implied.
- **In progress:** source code or configuration is being implemented; only completed and evidenced increments should be described as implemented.
- **CI + Docker + security verified:** the project's automated tests passed, its Docker image built, and Bandit plus pip-audit completed successfully in GitHub Actions. This is not production verification.

## Delivery rules

- Every project starts with written scope, assumptions and acceptance criteria.
- Prefer small increments that can be implemented and verified independently.
- Use synthetic or public sample data.
- Keep proposed architecture separate from implemented architecture.
- Record exact commands, results, limitations and unresolved decisions.
- Change a project status only when repository and execution evidence supports it.
- Do not claim production readiness, compliance or customer deployment without evidence.

## Portfolio integration sequence

The fifteen core domain projects have initial CI-verified prototype slices. The sixteenth Enterprise Portfolio Integration project now has an authenticated supplier-onboarding HTTP vertical slice across Document Intelligence and MDM. Its 13-test suite, Docker build and real three-service HTTP smoke test passed; enterprise identity, role-based authorization and tenant isolation remain future milestones.
