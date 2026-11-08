# Enterprise AI Engineering

A practical engineering portfolio exploring enterprise software development, AI coding agents, software quality, testing, Python data engineering and enterprise architecture.

This repository contains fifteen separately scoped project folders under `projects/` (not fifteen separate GitHub repositories). Each folder has a project overview, detailed blueprint, source-code boundaries, test strategy and local deployment plan. These documents establish the implementation scope; executable code and verification are tracked separately as they are completed.

## Integrated enterprise architecture

The portfolio's target-state architecture connects business strategy and operating model with enterprise data, integration, cloud engineering, AI agents, security, information resilience, observability and software delivery. See the [integrated enterprise reference architecture](docs/architecture/enterprise-reference-architecture.md), [capability map](docs/architecture/capability-map.md) and [module dependency map](docs/architecture/module-dependency-map.md).

## Documentation

See the [engineering documentation portal](docs/README.md) for architecture references, local setup, configuration, testing, operations, troubleshooting and project walkthroughs.

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

The fifteen projects are maintained as independent workstreams inside this single repository. Each project README now describes its business purpose, capabilities, reference workflow, key modules, demonstration scenario, guardrails, documentation and delivery status. Their blueprints define detailed architecture and acceptance criteria. Projects will be implemented and verified individually before a separate final project is designed to connect them.

| # | Independent project | Main capability | Status |
|---:|---|---|---|
| 1 | [Enterprise Information Resilience](projects/enterprise-information-resilience/README.md) | Digital trust, information integrity, reputation resilience | Specified |
| 2 | [Enterprise Document Intelligence](projects/enterprise-document-intelligence/README.md) | Document extraction, validation, human exception handling | Specified |
| 3 | [Breach-Resilient Enterprise](projects/breach-resilient-enterprise/README.md) | Zero trust, attack-path containment, response | Specified |
| 4 | [Enterprise Data Protection](projects/enterprise-data-protection/README.md) | Classification, minimisation, masking, access governance | Specified |
| 5 | [Enterprise Attention and Intelligence Hub](projects/enterprise-attention-intelligence-hub/README.md) | Business-impact observability and prioritisation | Specified |
| 6 | [Enterprise MDM and Data Governance](projects/enterprise-mdm-data-governance/README.md) | Matching, survivorship, stewardship, golden records | Specified |
| 7 | [Agent-Driven Enterprise Operations](projects/agent-driven-enterprise-operations/README.md) | Bounded agents, tool policy, human approvals | Specified |
| 8 | [Enterprise Integration Platform](projects/enterprise-integration-platform/README.md) | APIs, events, routing, orchestration, reliability | Specified |
| 9 | [Predictive Life Sciences Supply Chain](projects/predictive-life-sciences-supply-chain/README.md) | Supply visibility, traceability, risk prediction | Specified |
| 10 | [Pharma R&D Data Spine](projects/pharma-rnd-data-spine/README.md) | Research data harmonisation and lineage | Specified |
| 11 | [Cloud Data Engineering Platform](projects/cloud-data-engineering-platform/README.md) | Ingestion, lakehouse patterns, quality, FinOps | Specified |
| 12 | [Autonomous AI Engineering Workbench](projects/autonomous-ai-engineering-workbench/README.md) | Sandboxed coding-agent evaluation | Specified |
| 13 | [Third-Party Risk Management](projects/third-party-risk-management/README.md) | Vendor lifecycle, evidence, access and fourth-party risk | Specified |
| 14 | [SAP S/4HANA Data Modernisation](projects/sap-s4-data-modernisation/README.md) | SAP master data, migration, CDC and reconciliation | Specified |
| 15 | [Enterprise Architecture Assessment Toolkit](projects/enterprise-architecture-assessment-toolkit/README.md) | Capability-led assessment and target-state roadmap | Specified |

**Status meaning:** Specified means architecture and implementation guidance are documented. It does not mean executable implementation, tests, deployment or client integration are complete.

The earlier six project briefs remain in the repository as additional engineering exercises. They are not substitutes for the fifteen independent projects above.

## Project build sequence

1. Establish the individual project structure, domain contracts and acceptance criteria.
2. Implement each project independently, including source code, tests, security and local deployment.
3. Run and record project-level verification and demo evidence.
4. Only after the individual projects are stable, create the final portfolio integration project with explicit contracts and adapters between them.

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
│   └── enterprise-architecture-assessment-toolkit/
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

All fifteen project folders and their core specification files are present. The individual project overviews and the portfolio catalogue are documented. Executable application code, automated test runs, container builds, CI verification and deployment evidence remain pending unless explicitly recorded in a project.

## Portfolio implementation roadmap

See [docs/PORTFOLIO_IMPLEMENTATION_ROADMAP.md](docs/PORTFOLIO_IMPLEMENTATION_ROADMAP.md) for the delivery sequence, implementation gates, shared engineering standards and evidence required before a project is marked verified.
