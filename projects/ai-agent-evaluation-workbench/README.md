# Project 4: AI Agent Evaluation Workbench

- Status: Proposed
- Type: Evaluation framework and repeatable engineering exercises

## Problem context

A coding agent may produce a plausible explanation while introducing defects, missing requirements or weakening tests. Evaluation must focus on the resulting change and independently verified behaviour.

## Objectives

- Create a consistent task format for agent trials.
- Capture repository state, task prompt, model/version and tool permissions.
- Compare agent output with explicit acceptance criteria.
- Measure correctness, test coverage, regressions and human review effort.
- Preserve a clear distinction between generated and human-authored changes.

## Proposed evaluation lifecycle

1. Select a bounded ticket from the Java or Python project.
2. Record branch, starting commit, environment and baseline checks.
3. Prepare a task prompt with scope, constraints and acceptance criteria.
4. Run the agent and preserve its proposed diff and execution notes.
5. Review the diff independently; do not rely on agent self-assessment.
6. Run tests and relevant security/quality checks.
7. Record missed requirements, defects, regressions and human interventions.
8. Publish an evaluation report with limitations.

## Evaluation dimensions

- Requirement coverage and correctness.
- Edge-case handling and robustness.
- Test relevance and regression protection.
- Design consistency and maintainability.
- Security and privacy handling.
- Debugging and root-cause reasoning.
- Tool discipline, iteration count and human review effort.

## Acceptance criteria

- A trial can be repeated from a recorded starting commit.
- Prompt, model/version when known, tools and permissions are recorded.
- Generated and human-modified lines are distinguishable through history or notes.
- Every claimed test result has a command and captured evidence.
- Evaluation conclusions are supported by observed results.
- Comparisons disclose differences in model, configuration or environment.

## Deliverables

Task cards, prompt records, run logs, reviewed diffs, test evidence and evaluation reports. Do not publish confidential prompts, private source, credentials or customer information.
