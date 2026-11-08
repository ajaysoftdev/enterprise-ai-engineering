# Test strategy — Autonomous AI Engineering Workbench

## Test layers
1. Unit: state machine, permissions, scoring and lifecycle rules.
2. Application: workflow orchestration with fake agents and repositories.
3. Contract: task, tool, evidence and API schema validation.
4. Integration: sandbox, Git adapter and persistence.
5. End-to-end: synthetic flow covering Task specification → sandbox/worktree → agent run → tool/budget enforcement → test execution → diff/security review → scoring → report.
6. Security: sandbox escape attempts, path traversal, tool misuse, secret exposure and privilege boundaries.
7. Resilience: timeout, cancellation, crash, retry, duplicate request and partial evidence.

## Fixtures
Create synthetic Task, RepositorySnapshot, AgentProfile, Run, ToolCall, Patch, TestResult, ReviewFinding, Score, EvaluationReport fixtures. Include invalid permissions, malformed tasks, incomplete evidence and boundary budgets. Vendor workflow tests must use fictitious supplier records.

## Definition of done
Tasks are reproducible; tool policies are enforced; evidence is retained; scores can be recomputed from versioned rubrics; unsafe actions are blocked; CI retains test results.

## Current executable test slice
The current API suite covers health/task discovery, full static acceptance scoring, missing acceptance files, secret-pattern detection, unsafe execution-pattern detection, unknown task rejection and report persistence. No source code is executed; agent/model, sandbox escape, real test runner, cost budget and merge-control tests remain unimplemented.

## Evidence
Record commit, environment, agent/model version when used, tool policy, command, budgets, results and exclusions. Untested scenarios remain planned.
