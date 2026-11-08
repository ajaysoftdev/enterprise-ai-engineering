# Project Catalogue

This directory contains fifteen independently scoped enterprise project workstreams, plus six earlier engineering exercises. The fifteen portfolio projects each have a project overview, detailed blueprint, curated reference sources, implementation architecture, domain contracts/data model and delivery/test guidance.

The project folders are maintained inside this repository; they are not separate GitHub repositories.

## Fifteen enterprise portfolio projects

| # | Project | Primary business capability | Status |
|---:|---|---|---|
| 1 | [Enterprise Information Resilience](enterprise-information-resilience/README.md) | Digital trust, information integrity and reputation resilience | Specified |
| 2 | [Enterprise Document Intelligence](enterprise-document-intelligence/README.md) | Document extraction, validation and human exception handling | CI verified — 6 tests passed; text-only prototype limitations remain |
| 3 | [Breach-Resilient Enterprise](breach-resilient-enterprise/README.md) | Zero-trust architecture and attack-path containment | CI verified — 6 simulation tests passed; no live controls connected |
| 4 | [Enterprise Data Protection](enterprise-data-protection/README.md) | Data classification, minimisation, masking and access governance | CI verified — 7 synthetic policy/masking tests passed; limitations remain |
| 5 | [Enterprise Attention and Intelligence Hub](enterprise-attention-intelligence-hub/README.md) | Business-impact observability and decision prioritisation | CI verified — 6 synthetic scoring/correlation tests passed; limitations remain |
| 6 | [Enterprise MDM and Data Governance](enterprise-mdm-data-governance/README.md) | Matching, survivorship, stewardship and golden records | CI verified — 6 tests passed; prototype limitations remain |
| 7 | [Agent-Driven Enterprise Operations](agent-driven-enterprise-operations/README.md) | Bounded agents, policy checks and human approvals | CI verified — 7 policy/approval tests passed; no live agent tools connected |
| 8 | [Enterprise Integration Platform](enterprise-integration-platform/README.md) | APIs, events, routing, orchestration and reliability | Specified |
| 9 | [Predictive Life Sciences Supply Chain](predictive-life-sciences-supply-chain/README.md) | Supply visibility, lot traceability and risk prediction | Specified |
| 10 | [Pharma R&D Data Spine](pharma-rnd-data-spine/README.md) | Research data harmonisation, traceability and lineage | Specified |
| 11 | [Cloud Data Engineering Platform](cloud-data-engineering-platform/README.md) | Ingestion, lakehouse transformations, quality and FinOps | Specified |
| 12 | [Autonomous AI Engineering Workbench](autonomous-ai-engineering-workbench/README.md) | Sandboxed coding-agent evaluation and evidence reporting | Specified |
| 13 | [Third-Party Risk Management](third-party-risk-management/README.md) | Vendor lifecycle, due diligence and fourth-party risk | Specified |
| 14 | [SAP S/4HANA Data Modernisation](sap-s4-data-modernisation/README.md) | SAP-like master data migration and reconciliation | Specified |
| 15 | [Enterprise Architecture Assessment Toolkit](enterprise-architecture-assessment-toolkit/README.md) | Capability-led assessment and target-state roadmapping | Specified |

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
- **Verified:** the relevant commands and automated checks have actually run, and their results are recorded.

## Delivery rules

- Every project starts with written scope, assumptions and acceptance criteria.
- Prefer small increments that can be implemented and verified independently.
- Use synthetic or public sample data.
- Keep proposed architecture separate from implemented architecture.
- Record exact commands, results, limitations and unresolved decisions.
- Change a project status only when repository and execution evidence supports it.
- Do not claim production readiness, compliance or customer deployment without evidence.

## Portfolio integration sequence

The fifteen projects will be implemented and verified independently. A separate sixteenth integration project is intentionally deferred until the individual projects have stable interfaces, data contracts, identity and access patterns, and operational evidence.
