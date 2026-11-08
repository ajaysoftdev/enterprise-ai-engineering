# Autonomous AI Engineering Workbench

**Purpose:** Evaluate AI coding agents through reproducible engineering tasks, isolated execution, controlled tools and evidence-based quality scoring.

**Domain:** AI-assisted software engineering, agent evaluation and developer productivity.  
**Technology direction:** Python orchestration, isolated worktrees/containers, provider-neutral model adapters and automated quality tools; concrete choices will be recorded as ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No agent benchmark result, model ranking or autonomous merge capability is claimed until implemented and reproducibly tested.