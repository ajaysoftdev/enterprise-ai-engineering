# Agent-Driven Enterprise Operations

**Purpose:** Coordinate enterprise tasks through AI agents with bounded authority, explicit policy checks, durable workflows and human approval for consequential actions.

**Domain:** Agentic AI, workflow orchestration and enterprise operations.  
**Technology direction:** Provider-neutral LLM and tool adapters, policy enforcement, durable workflow state and auditable APIs; concrete choices will be captured in ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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
