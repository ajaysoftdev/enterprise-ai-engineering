# Enterprise Capability Map

This map groups the capabilities required by the integrated enterprise reference architecture. It is a planning model, not a claim that every capability is implemented.

## 1. Business and transformation

| Capability | Key outputs |
|---|---|
| Strategy and outcome definition | Business outcomes, measures and investment themes |
| Business architecture | Capability map, value streams, process ownership |
| Operating model design | Roles, decision rights, human/agent responsibilities |
| Enterprise architecture | Current state, target state, principles, standards and roadmap |
| Portfolio and change governance | Prioritised initiatives, dependencies, transition states and architecture decisions |

## 2. Enterprise information management

| Capability | Key outputs |
|---|---|
| Data governance | Owners, stewards, policies, standards and decision rights |
| Master data management | Golden records, matching, survivorship and distribution |
| Reference data management | Controlled code sets and hierarchies |
| Data quality management | Rules, scores, exceptions, remediation and reconciliation |
| Metadata and lineage | Catalog, classification, provenance and impact analysis |
| Semantic management | Shared business terms, KPI definitions and data contracts |
| Data platform engineering | Ingestion, transformation, storage, serving and data products |

## 3. Integration and process

| Capability | Key outputs |
|---|---|
| API management | API standards, gateway policies, lifecycle and developer access |
| Event management | Event taxonomy, schemas, broker standards and subscriptions |
| Data movement | Batch, CDC, streaming and controlled file transfer |
| Workflow management | State, approvals, timers, escalation and compensation |
| Transaction integrity | Idempotency, correlation, reconciliation and exception queues |
| Partner integration | Onboarding, contracts, identity and operational support |

## 4. AI and intelligent automation

| Capability | Key outputs |
|---|---|
| Inference services | Extraction, classification, summarisation and recommendations |
| Knowledge grounding | Approved retrieval sources, citations and freshness controls |
| Agent orchestration | Planning, tool selection, bounded execution and escalation |
| Agent identity and permissions | Per-agent identity, scopes, policies and revocation |
| AI evaluation | Test sets, quality measures, adversarial tests and regression evidence |
| Model and prompt lifecycle | Versioning, approval, deployment, monitoring and rollback |
| Human oversight | Review queues, overrides, approvals and accountability |

## 5. Cybersecurity, privacy and trust

| Capability | Key outputs |
|---|---|
| Identity and access management | Authentication, authorisation and lifecycle management |
| Privileged access management | Just-in-time access, session oversight and emergency access |
| Application and API security | Secure design, object-level access and abuse protection |
| Data protection | Classification, encryption, masking, tokenisation and retention |
| Cloud and workload security | Segmentation, posture management and runtime controls |
| Secure delivery and supply chain | Scanning, artifact signing, SBOM and deployment policy |
| Third-party risk management | Vendor tiering, assurance, access review and offboarding |
| AI security and governance | Threat models, tool boundaries, data-use policy and action controls |
| Information integrity | Provenance assessment, evidence handling and response coordination |

## 6. Operations and resilience

| Capability | Key outputs |
|---|---|
| Observability | Logs, metrics, traces and business-service correlation |
| Event and alert management | Deduplication, prioritisation and routing |
| AIOps | Anomaly detection, event correlation and decision support |
| Incident management | Ownership, response procedures and evidence |
| Business continuity | Business impact analysis, RTO/RPO and recovery plans |
| Recovery engineering | Isolated backups, clean recovery and restore tests |
| FinOps and capacity | Cost allocation, optimisation and workload efficiency |

## 7. Software and platform engineering

| Capability | Key outputs |
|---|---|
| Application engineering | Services, interfaces and maintainable code |
| Data engineering | Reproducible pipelines and data products |
| Platform engineering | Environments, reusable runtime services and templates |
| DevSecOps | CI/CD, automated controls and release evidence |
| Quality engineering | Unit, integration, contract, performance and security tests |
| Architecture governance | ADRs, design reviews, standards and exceptions |
| Developer productivity | Local setup, tooling, documentation and engineering workflows |

## 8. Shared foundational services

These should be designed once where practical and reused through stable contracts:

- Enterprise identity and policy enforcement.
- Secrets and key management.
- API and event contracts.
- Correlation and audit-event conventions.
- Data classification and metadata standards.
- Workflow and human approval patterns.
- Observability instrumentation and service catalog.
- CI/CD templates, infrastructure modules and security gates.
- Agent tool registry, evaluation harness and policy checks.

## 9. Capability ownership

Each capability needs an accountable business or technology owner, a service owner where applicable, defined consumers, operating measures and a lifecycle. Shared services should not become ownerless central bottlenecks; domain teams remain accountable for their data, APIs, events and business outcomes.
