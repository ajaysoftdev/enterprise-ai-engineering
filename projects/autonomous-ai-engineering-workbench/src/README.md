# Source-code layout — Autonomous AI Engineering Workbench

```text
src/
  aiworkbench/
    main.py              # task catalogue and evaluation API
    models.py            # typed patch and report contracts
    tasks.py             # versioned deterministic benchmark registry
    evaluator.py         # static acceptance and security-pattern checks
    repository.py        # SQLite evaluation report persistence
  app/                  # config, composition and health
  api/
    routes/             # versioned endpoints
    schemas/            # task/evidence contracts
  domain/
    entities.py         # Task, RepositorySnapshot, AgentProfile, Run, ToolCall, Patch, TestResult, ReviewFinding, Score, EvaluationReport
    policies.py         # invariants and permissions
    state_machine.py    # valid lifecycle transitions
  application/
    commands/           # submit, execute, approve, assess, report
    ports.py             # agent/Git/sandbox/vendor-system interfaces
  infrastructure/
    adapters/           # task_catalog, sandbox, git_adapter, agent_adapter, tool_policy, runner, test_harness, diff_review, scoring, report
    persistence/        # repositories and migrations
    sandbox/            # isolated execution implementation
  evaluation/           # test harness, scoring and evidence
  observability/        # logs, metrics and traces
```

## Engineering rules
- No untrusted code execution outside an isolated sandbox.
- Enforce tool allowlists, timeouts, token/cost budgets and cancellation.
- Preserve original inputs, diffs, logs and test evidence.
- Make scoring explainable and version evaluation rubrics.
- Do not treat a model assertion as proof of a test result.
- Keep secrets out of prompts, logs and artifacts.

## First executable milestone
Implement one deterministic task, a fake agent adapter, isolated temporary workspace, command runner, result schema and tests. Live model/provider execution is a later adapter.
