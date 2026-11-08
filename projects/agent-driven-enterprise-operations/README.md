# Agent-Driven Enterprise Operations

**Purpose:** Coordinate enterprise tasks through AI agents with bounded authority, explicit policy checks, durable workflows and human approval for consequential actions.

**Domain:** Agentic AI, workflow orchestration and enterprise operations.  
**Technology direction:** Provider-neutral LLM and tool adapters, policy enforcement, durable workflow state and auditable APIs; concrete choices will be captured in ADRs.  
**Status:** Current prototype CI + Docker + security verified — 8 tests passed on Python 3.12 (GitHub Actions run 42461086864, commit 05b8198). This verifies the synthetic prototype scope only; production readiness is not claimed.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Register agents, tools, scopes and permitted actions.
- Convert requests into bounded, observable work plans.
- Enforce identity, policy, budget and tool-use constraints.
- Execute long-running workflows with retries and persisted state.
- Pause for human approval before sensitive or irreversible actions.
- Record prompts, tool calls, decisions, outcomes and exceptions.

## Reference workflow
Request intake → intent and scope validation → plan proposal → policy evaluation → bounded tool execution → approval checkpoint → completion or exception → audit and outcome review.

## Key modules
- **Agent registry:** agent identity, role, version and allowed capabilities.
- **Tool registry:** schemas, permissions, rate limits and risk classification.
- **Policy gateway:** authorisation, approval and execution constraints.
- **Orchestrator:** durable state, retries, deadlines and compensation.
- **Human review:** approval, rejection, escalation and override.
- **Audit and evaluation:** trace, cost, quality and policy-compliance evidence.

## Expected demonstration
Run a synthetic procurement or service-desk workflow in which an agent can gather information and prepare an action but must obtain explicit approval before committing a purchase or changing a business record.

## Guardrails
Treat retrieved content and tool output as untrusted. Prevent prompt injection from granting authority. Apply least privilege, sandbox tools, cap cost/time, maintain idempotency and provide a kill switch.

## First executable slice

The current prototype implements an allow-listed procurement workflow planner, a fixed tool registry, risk classification, policy decisions, SQLite workflow/audit persistence and human approval/rejection. Read-only supplier lookup can be prepared; purchase-order drafting/submission pauses for approval; destructive supplier deletion is blocked. Approval changes state to `APPROVED_DRY_RUN` only and never submits an order.

**Limitations:** there is no LLM/agent runtime, live tool execution, enterprise identity, role-based approver authorization, tenant isolation, durable distributed orchestration, budget enforcement, external procurement connector or production kill switch. The policy is a deterministic prototype. Request text is stored as untrusted input and does not grant tools or permissions. GitHub Actions executed the API suite successfully: 7 passed, 0 failed. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn agentops.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No autonomous production actions, enterprise agent deployment or measured productivity gain is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
