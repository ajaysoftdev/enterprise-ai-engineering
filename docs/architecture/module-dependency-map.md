# Portfolio Module Dependency Map

## 1. Purpose

This document translates the enterprise reference architecture into implementable portfolio modules. Modules are logical workstreams and do not automatically require separate repositories or deployable services.

## 2. Modules

| ID | Module | Main scope | Primary dependencies |
|---|---|---|---|
| M0 | Architecture and governance workbench | Capability maps, architecture decisions, risks, target state and roadmap | None; defines standards for all modules |
| M1 | Enterprise data foundation | Data contracts, quality, MDM patterns, lineage and synthetic data | M0 |
| M2 | Integration and workflow foundation | APIs, events, CDC patterns, retries, idempotency and reconciliation | M0, M1 |
| M3 | Cloud data engineering | Batch/stream pipelines, lakehouse patterns, orchestration and DataOps | M0, M1, M2 |
| M4 | AI inference and knowledge services | Document inference, RAG, evaluation and model lifecycle | M0, M1, M2 |
| M5 | Agentic workflow platform | Tool registry, bounded agents, approval, execution and audit | M1, M2, M4, M6 |
| M6 | Security and trust foundation | Identity, access policy, secrets, threat models, privacy and supply-chain controls | M0; shared by all modules |
| M7 | Observability and AIOps | Telemetry, correlation, alert prioritisation and recovery support | M1, M2, M3, M4, M5, M6 |
| M8 | Information resilience | Source provenance, information-risk signals, evidence cases and response workflow | M2, M4, M5, M6, M7 |
| M9 | Engineering quality platform | Test automation, CI/CD, code review, IaC checks and evidence | M0, M6; applied across all modules |
| M10 | Industry reference scenarios | Supplier onboarding, life-sciences traceability, supply-chain exception and other process demonstrations | M1-M9 as required by scenario |

## 3. Dependency view

- M0 Architecture -> M1 Data -> M2 Integration -> M3 Data Engineering
- M1 Data + M2 Integration + M6 Security -> M4 Inference and Knowledge
- M2 Integration + M4 AI + M6 Security -> M5 Agentic Workflows
- M1-M6 -> M7 Observability and AIOps
- M2 + M4 + M5 + M6 + M7 -> M8 Information Resilience
- M6 Security + M9 Engineering Quality -> delivery controls across all modules
- M10 Industry Scenarios -> exercise and validate the relevant capabilities end to end

## 4. Shared contracts and reusable components

- Identity context and authorisation decision interface.
- API standards, event envelope and schema versioning.
- Business entity identifiers and master-data contracts.
- Correlation ID and audit-event schema.
- Data quality rule interface and exception format.
- Workflow task, approval and escalation contract.
- Agent tool manifest and permission policy.
- Model evaluation case format and result record.
- Observability conventions and service ownership metadata.

## 5. Repository strategy

Use the existing enterprise-ai-engineering repository as the central portfolio hub for architecture, shared standards, project specifications, engineering tickets, evaluation evidence and cross-module documentation.

Use the existing spring-petclinic fork as a separate application codebase for Java/Spring engineering, testing, security and delivery exercises. Keep upstream application code and attribution distinct from original portfolio documentation and changes.

Do not create one repository per capability at this stage. Split a module into its own repository only when there is a clear independent lifecycle, reusable consumer base, separate deployment boundary, distinct permissions or meaningful maintenance need.

## 6. Suggested implementation sequence

### Stage 0 — Baseline and architecture controls
- Inspect current repository contents and identify existing reusable work.
- Define naming, status, testing, security and evidence conventions.
- Establish architecture decision and engineering ticket templates.

### Stage 1 — Working application and delivery baseline
- Set up the local Java toolchain.
- Build and run the existing Spring PetClinic application.
- Record baseline tests and runtime observations.
- Add bounded enhancements with tests and code-review evidence.

### Stage 2 — Data and integration foundation
- Implement a small synthetic-data pipeline.
- Add schema contracts, validation, quarantine and reconciliation.
- Expose a bounded API and publish a business event.
- Demonstrate retry, duplicate and failure handling.

### Stage 3 — Inference and knowledge
- Add a document-processing use case using synthetic documents.
- Ground answers in approved sample content.
- Build evaluation cases and measure extraction, grounding and escalation quality.

### Stage 4 — Bounded agent workflow
- Connect an agent to allowlisted tools and synthetic business records.
- Start in recommendation/draft mode.
- Add policy checks, approval, idempotency, audit and rollback/compensation behaviour before enabling any write action.

### Stage 5 — Security, observability and resilience
- Add identity and least-privilege patterns, secret handling and threat tests.
- Correlate traces across API, workflow, pipeline and agent steps.
- Demonstrate alert prioritisation, incident response and recovery exercises.

### Stage 6 — Integrated industry scenarios
- Combine the modules in supplier onboarding and supply-chain exception scenarios.
- Add a life-sciences traceability scenario using synthetic entities and events.
- Add information-integrity monitoring as a controlled case-management exercise, not automated truth adjudication.

## 7. Completion evidence

A module is not complete because its design document exists. Completion requires, as applicable:

- Source code and reproducible setup.
- Automated tests and recorded execution results.
- Threat model and security checks.
- Architecture decisions and interface contracts.
- Operational instructions and failure/recovery exercises.
- Demonstration data that is synthetic or appropriately public.
- Clear status labels and known limitations.

## 8. Project implementation mapping

The current 15 prototype workstreams map to these logical modules:

| Portfolio project | Module alignment |
|---|---|
| Enterprise Architecture Assessment Toolkit | M0 — architecture and governance workbench |
| Enterprise MDM and Data Governance; Pharma R&D Data Spine | M1 — enterprise data foundation |
| Enterprise Integration Platform; SAP S/4HANA Data Modernisation | M2 — integration and workflow foundation |
| Cloud Data Engineering Platform; Predictive Life Sciences Supply Chain | M3 — cloud data engineering and industry scenarios |
| Enterprise Document Intelligence | M4 — inference and knowledge services |
| Agent-Driven Enterprise Operations; Autonomous AI Engineering Workbench | M5 — agentic workflow and engineering workbench |
| Breach-Resilient Enterprise; Enterprise Data Protection; Third-Party Risk Management | M6 — security and trust foundation |
| Enterprise Attention and Intelligence Hub | M7 — observability and AIOps |
| Enterprise Information Resilience | M8 — information resilience |
| All 15 project CI workflows and shared engineering standards | M9 — engineering quality platform |
| Life Sciences Supply Chain, Pharma R&D, SAP Modernisation and TPRM scenarios | M10 — industry reference scenarios |

For project-to-project producer/consumer handoffs, shared event envelopes, API conventions and integration acceptance criteria, see the [Portfolio Integration Contract Register](../PORTFOLIO_INTEGRATION_CONTRACT_REGISTER.md).

## 9. Status

The 15 project folders now contain independent executable synthetic prototypes, API contracts, automated tests, Docker packaging and CI workflows. Initial CI and Docker evidence is recorded in the project catalogue. A later revision added request-correlation middleware and tests across all 15 services; the current-revision CI reruns are pending. The shared portfolio integration is still a separate future workstream; it is not yet implemented.
