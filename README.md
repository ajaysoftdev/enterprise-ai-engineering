# Enterprise AI Engineering

A practical engineering portfolio exploring enterprise software development, AI coding agents, software quality, testing, Python data engineering and architecture.

The portfolio is organised around end-to-end projects. Each project starts with a problem statement and acceptance criteria, then progresses through implementation, testing, review and evidence-based reporting.

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

## Project catalogue

| Project | Main skills | Status |
|---|---|---|
| [Spring PetClinic service enhancement](projects/java-spring-petclinic/README.md) | Java, Spring Boot, REST, persistence, debugging, tests | Proposed |
| [Python batch data pipeline](projects/python-batch-data-pipeline/README.md) | Python, ingestion, transformation, error handling, tests | Proposed |
| [Data quality framework](projects/data-quality-framework/README.md) | Profiling, validation, data contracts, quarantine, reporting | Proposed |
| [AI agent evaluation workbench](projects/ai-agent-evaluation-workbench/README.md) | Task design, agent runs, diff review, evaluation metrics | Proposed |
| [Quality automation pipeline](projects/quality-automation-pipeline/README.md) | CI, automated tests, static checks, dependency hygiene | Proposed |
| [Enterprise integration architecture case study](projects/enterprise-integration-architecture/README.md) | Architecture, APIs, events, reliability, security, ADRs | Proposed |

These are project specifications, not claims that the implementations or tests are already complete. Status will change only when supported by commits and execution evidence.

## Repository structure

```text
enterprise-ai-engineering/
├── java-engineering/
├── python-data-engineering/
├── ai-coding-agent-evaluation/
├── code-review/
├── testing-and-quality/
├── engineering-tickets/
├── evaluation-reports/
├── architecture/
├── projects/
│   ├── java-spring-petclinic/
│   ├── python-batch-data-pipeline/
│   ├── data-quality-framework/
│   ├── ai-agent-evaluation-workbench/
│   ├── quality-automation-pipeline/
│   └── enterprise-integration-architecture/
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

Portfolio structure, project specifications and working templates are being established. The six project briefs are proposed work. Local setup, implementation, test execution and agent comparisons remain pending until actually performed and documented.
