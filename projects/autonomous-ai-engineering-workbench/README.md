# Autonomous AI Engineering Workbench

**Purpose:** Evaluate AI coding agents through reproducible engineering tasks, isolated execution, controlled tools and evidence-based quality scoring.

**Domain:** AI-assisted software engineering, agent evaluation and developer productivity.  
**Technology direction:** Python orchestration, isolated worktrees/containers, provider-neutral model adapters and automated quality tools; concrete choices will be recorded as ADRs.  
**Status:** Static-evaluation prototype CI verified — 7 tests passed on Python 3.12 (GitHub Actions run 42455321589, commit 0d27774). This verifies text-only checks; no agent execution, sandboxing or test-runner validation is claimed.

## Business capabilities
- Define benchmark tasks with scope, acceptance criteria and test fixtures.
- Execute agents in isolated workspaces with constrained permissions.
- Register tools, enforce time/token/cost budgets and capture tool activity.
- Run unit, integration, lint, security and regression checks.
- Review generated diffs for correctness, security and maintainability.
- Score outcomes with reproducible evidence and limitations.

## Reference workflow
Task specification → isolated sandbox/worktree → agent run → tool and budget enforcement → test execution → diff/security review → scoring → evidence report.

## Key modules
- **Task registry:** benchmark definition, fixtures and acceptance criteria.
- **Agent adapters:** model/provider-neutral execution interface.
- **Sandbox manager:** isolated workspace, resource limits and cleanup.
- **Tool gateway:** allowlists, permissions, logging and budgets.
- **Quality runner:** tests, static analysis and security checks.
- **Evaluator:** weighted scoring, comparison and report generation.

## Expected demonstration
Run the same bounded bug-fix task with two agent configurations in isolated workspaces, compare test outcomes and diffs, and generate a report that records the exact evaluation conditions.

## Guardrails
Never expose host secrets or unrestricted shell access. Treat repository content and tool output as untrusted. Require human review before merging or deploying agent-generated changes.

## First executable slice

The current prototype contains a versioned benchmark-task registry, a static patch evaluator, acceptance-marker checks, secret-pattern and unsafe-execution-pattern detection, weighted evidence scoring, SQLite report persistence, API tests, OpenAPI, Docker and GitHub Actions.

**Important limitations:** submitted source is inspected as text and is never executed. No LLM provider, coding agent, Git worktree, container sandbox, shell runner, test runner, cost/token budget enforcement or human code-review workflow is connected. The report explicitly marks test execution as `NOT_RUN`; a high static score is not proof that code works or is safe to merge. The security patterns are illustrative and are not a substitute for a security scanner. GitHub Actions executed the API suite successfully: 7 passed, 0 failed. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn aiworkbench.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No agent benchmark result, model ranking or autonomous merge capability is claimed until implemented and reproducibly tested.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
