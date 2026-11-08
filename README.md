# Enterprise AI Engineering

A practical engineering portfolio exploring enterprise software development, AI coding agents, software quality, testing, Python data engineering and enterprise architecture.

This repository contains fifteen core domain projects plus a sixteenth portfolio integration project under `projects/` (all within this single GitHub repository). Each project now includes its own executable synthetic prototype, API contract, automated tests, Docker configuration and CI workflow, alongside its architecture and domain documentation. Current verification is limited to the documented prototype scope; production integrations and security assurance remain separate delivery gates.

## Integrated enterprise architecture

The portfolio's target-state architecture connects business strategy and operating model with enterprise data, integration, cloud engineering, AI agents, security, information resilience, observability and software delivery. See the [integrated enterprise reference architecture](docs/architecture/enterprise-reference-architecture.md), [capability map](docs/architecture/capability-map.md) and [module dependency map](docs/architecture/module-dependency-map.md).

## Documentation

See the [engineering documentation portal](docs/README.md) for architecture references, local setup, configuration, testing, operations, troubleshooting and project walkthroughs. Also see the [portfolio implementation roadmap](docs/PORTFOLIO_IMPLEMENTATION_ROADMAP.md), [portfolio security baseline](docs/PORTFOLIO_SECURITY_BASELINE.md) and [portfolio integration contract register](docs/PORTFOLIO_INTEGRATION_CONTRACT_REGISTER.md). Repository governance is documented in [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md); pull requests use a structured [review template](.github/pull_request_template.md).

## Portfolio areas

| Area | Focus | Project links |
|---|---|---|
| [Java Engineering](java-engineering/README.md) | Java, Spring Boot, REST APIs, debugging and refactoring | [PetClinic service enhancement](projects/java-spring-petclinic/README.md) |
| [Python Data Engineering](python-data-engineering/README.md) | Ingestion, transformation, validation and automation | [Batch data pipeline](projects/python-batch-data-pipeline/README.md) |
| Data Quality | Validation rules, profiling, quarantine and reporting | [Data quality framework](projects/data-quality-framework/README.md) |
| [AI Coding Agent Evaluation](ai-coding-agent-evaluation/README.md) | Controlled evaluation of AI-assisted engineering | [Agent evaluation workbench](projects/ai-agent-evaluation-workbench/README.md) |
| [Code Review](code-review/README.md) | Correctness, security, maintainability and operational review | Applied across all projects |
| [Testing and Quality](testing-and-quality/README.md) | Unit, integration, API, regression and CI checks | [Quality automation pipeline](projects/quality-automation-pipeline/README.md) |
| [Engineering Tickets](engineering-tickets/README.md) | Bounded bugs, features and acceptance criteria | Tickets will drive each project |
| [Evaluation Reports](evaluation-reports/README.md) | Reproducible engineering and agent reports | Evidence from each project |
| [Architecture](architecture/README.md) | Context, components, data flows, trade-offs and ADRs | [Enterprise integration case study](projects/enterprise-integration-architecture/README.md) |

## Independent project catalogue

The fifteen core projects are maintained as independent workstreams, with a sixteenth project composing them through explicit contracts. Each project README describes its business purpose, capabilities, reference workflow, key modules, demonstration scenario, guardrails, documentation and delivery status. Each also has a runnable prototype slice and project-level CI evidence. The portfolio integration project has now started its first vertical slice: supplier invoice intake → Document Intelligence → MDM, with idempotency and a human-stewardship pause.

| # | Independent project | Main capability | Status |
|---:|---|---|---|
| 1 | [Enterprise Information Resilience](projects/enterprise-information-resilience/README.md) | Digital trust, information integrity, reputation resilience | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478814374) |
| 2 | [Enterprise Document Intelligence](projects/enterprise-document-intelligence/README.md) | Document extraction, validation, human exception handling | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478818147) |
| 3 | [Breach-Resilient Enterprise](projects/breach-resilient-enterprise/README.md) | Zero trust, attack-path containment, response | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478821593) |
| 4 | [Enterprise Data Protection](projects/enterprise-data-protection/README.md) | Classification, minimisation, masking, access governance | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478825871) |
| 5 | [Enterprise Attention and Intelligence Hub](projects/enterprise-attention-intelligence-hub/README.md) | Business-impact observability and prioritisation | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478830047) |
| 6 | [Enterprise MDM and Data Governance](projects/enterprise-mdm-data-governance/README.md) | Matching, survivorship, stewardship, golden records | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478842872) |
| 7 | [Agent-Driven Enterprise Operations](projects/agent-driven-enterprise-operations/README.md) | Bounded agents, tool policy, human approvals | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478847750) |
| 8 | [Enterprise Integration Platform](projects/enterprise-integration-platform/README.md) | APIs, events, routing, orchestration, reliability | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478852405) |
| 9 | [Predictive Life Sciences Supply Chain](projects/predictive-life-sciences-supply-chain/README.md) | Supply visibility, traceability, risk prediction | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478856948) |
| 10 | [Pharma R&D Data Spine](projects/pharma-rnd-data-spine/README.md) | Research data harmonisation and lineage | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478860840) |
| 11 | [Cloud Data Engineering Platform](projects/cloud-data-engineering-platform/README.md) | Ingestion, lakehouse patterns, quality, FinOps | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478872883) |
| 12 | [Autonomous AI Engineering Workbench](projects/autonomous-ai-engineering-workbench/README.md) | Sandboxed coding-agent evaluation | CI + Docker + security verified — 10 tests passed (GitHub Actions run 42478877471) |
| 13 | [Third-Party Risk Management](projects/third-party-risk-management/README.md) | Vendor lifecycle, evidence, access and fourth-party risk | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478881646) |
| 14 | [SAP S/4HANA Data Modernisation](projects/sap-s4-data-modernisation/README.md) | SAP master data, migration, CDC and reconciliation | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478886356) |
| 15 | [Enterprise Architecture Assessment Toolkit](projects/enterprise-architecture-assessment-toolkit/README.md) | Capability-led assessment and target-state roadmap | CI + Docker + security verified — 9 tests passed (GitHub Actions run 42478891292) |
| 16 | [Enterprise Portfolio Integration](projects/enterprise-portfolio-integration/README.md) | Cross-project orchestration, idempotency and workflow traceability | CI + Docker + authenticated HTTP E2E + security verified — 13 tests passed (GitHub Actions run 42478896221) |

**Status meaning:** CI + Docker + security verified means the project's automated tests passed, its container image built, and Bandit plus pip-audit completed successfully in GitHub Actions. It does not mean production readiness, live enterprise integration beyond the documented HTTP slice, penetration-test clearance, regulatory validation or deployment to a customer environment.

The earlier six project briefs remain in the repository as additional engineering exercises. They are not substitutes for the sixteen portfolio projects above.

## Project build sequence

1. Establish the individual project structure, domain contracts and acceptance criteria.
2. Implement each project independently, including source code, tests, security and local deployment.
3. Run and record project-level verification and demo evidence.
4. The portfolio integration project is now started; expand its vertical slices only after the relevant domain contracts, adapter behaviour and end-to-end verification are stable.

## Repository structure

```text
enterprise-ai-engineering/
├── projects/
│   ├── enterprise-information-resilience/
│   ├── enterprise-document-intelligence/
│   ├── breach-resilient-enterprise/
│   ├── enterprise-data-protection/
│   ├── enterprise-attention-intelligence-hub/
│   ├── enterprise-mdm-data-governance/
│   ├── agent-driven-enterprise-operations/
│   ├── enterprise-integration-platform/
│   ├── predictive-life-sciences-supply-chain/
│   ├── pharma-rnd-data-spine/
│   ├── cloud-data-engineering-platform/
│   ├── autonomous-ai-engineering-workbench/
│   ├── third-party-risk-management/
│   ├── sap-s4-data-modernisation/
│   ├── enterprise-architecture-assessment-toolkit/
│   └── enterprise-portfolio-integration/
├── architecture/
├── java-engineering/
├── python-data-engineering/
├── ai-coding-agent-evaluation/
├── testing-and-quality/
└── docs/
```

## Open-source codebase and attribution

The Java engineering exercises use a fork of [Spring PetClinic](https://github.com/spring-projects/spring-petclinic), based on the canonical upstream project. Spring PetClinic is an existing open-source sample application, not an application originally authored for this portfolio. Upstream authorship and contributions remain with their respective owners and contributors.

See [third-party notices](docs/THIRD_PARTY_NOTICES.md) for attribution information.

## Working principles

- Start by understanding the existing code and its conventions.
- Define bounded scope and acceptance criteria before implementation.
- Establish a baseline before changing code.
- Verify changes through tests and other relevant checks.
- Record evidence, limitations and unresolved questions.
- Distinguish original work from adapted, open-source and AI-assisted work.
- Never claim a test, implementation or evaluation is complete without evidence.
- Use synthetic or public data only; never commit confidential code, credentials, tokens or personal data.

## Current status

All sixteen current-revision prototype CI suites passed: 152 tests across the portfolio, and all sixteen Docker images built successfully in GitHub Actions. All 16 APIs now enforce API-key authentication on non-health routes, propagate correlation IDs and return baseline security response headers. The integration adapters forward separate downstream API keys. The first three-service HTTP vertical slice (Document Intelligence → MDM → Portfolio Integration) also passed, including a steward decision and workflow refresh. Bandit static analysis and pip-audit passed for all 16 projects in GitHub Actions security matrix run 42478896241 (16/16 jobs). The initial pytest vulnerability was resolved by upgrading the development dependency to the patched release range. The prototypes use synthetic data and local SQLite-backed demonstrations where applicable. No production deployment, external system connection, independent security assessment or compliance validation is claimed.

## Portfolio implementation roadmap

See [docs/PORTFOLIO_IMPLEMENTATION_ROADMAP.md](docs/PORTFOLIO_IMPLEMENTATION_ROADMAP.md) for the delivery sequence, implementation gates, shared engineering standards and evidence required before a project is marked verified.
