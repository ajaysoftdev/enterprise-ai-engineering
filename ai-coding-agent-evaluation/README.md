# AI Coding Agent Evaluation

A structured approach to evaluating coding agents on bounded software-engineering tasks.

## Featured project

[AI agent evaluation workbench](../projects/ai-agent-evaluation-workbench/README.md)

The workbench will define a repeatable process for selecting tasks, capturing prompts and environment details, collecting diffs, running independent checks and recording human review effort. Initial evaluations will use the portfolio's Java and Python project tickets.

## Evaluation workflow

1. Define a reproducible engineering task and acceptance criteria.
2. Record the repository state, environment and baseline test results.
3. Give the agent the same task context and constraints for each trial.
4. Inspect the proposed diff rather than relying on the agent's explanation.
5. Run relevant tests and additional checks independently.
6. Record defects, regressions, omissions and human review effort.
7. Publish a concise report with evidence and limitations.

## Evaluation dimensions

- Requirement understanding and task completion
- Correctness and edge-case handling
- Test quality and regression coverage
- Maintainability and consistency with existing design
- Security and data-handling considerations
- Debugging quality and explanation of root cause
- Tool use, iteration efficiency and human intervention required

## Fairness and integrity

Record the agent, model/version when available, date, prompt/task, tools and configuration. Do not compare results from materially different conditions as if they were controlled trials. Distinguish agent-generated changes from human modifications. Do not publish private prompts, credentials, customer data or proprietary source code.

## Status

Evaluation framework and project specification documented; no comparative agent results are published yet.
