# Project 1: Spring PetClinic Service Enhancement

- Status: Proposed
- Type: Existing open-source application exercise
- Base code: [Portfolio fork](https://github.com/ajaysoftdev/spring-petclinic) of [Spring PetClinic upstream](https://github.com/spring-projects/spring-petclinic)

## Problem context

Use a familiar domain application to practise navigating an existing Java codebase and delivering a small, reviewable change without rewriting the application.

## Objectives

- Map the request path through controller, service and persistence layers.
- Understand the domain model and existing validation conventions.
- Deliver one narrowly scoped API or user-workflow enhancement.
- Add regression tests and document design choices.
- Review a separately generated AI-assisted change against the same criteria.

## Candidate increments

1. **Codebase map:** document entry point, packages, key entities, controllers, services, repositories and test layout.
2. **Baseline:** verify the supported JDK/build wrapper, run existing tests and record the exact result.
3. **Bounded enhancement:** choose a real gap confirmed in the code, such as an additional search/filter capability or clearer validation response. Confirm existing behaviour before selecting the change.
4. **Regression coverage:** add focused tests for normal, boundary and invalid input.
5. **Review:** inspect correctness, security, maintainability and compatibility.
6. **Agent trial:** give an AI coding agent the same ticket and independently inspect its diff.

## Acceptance criteria

- The selected behaviour is supported by a ticket with reproducible context.
- The implementation follows existing project conventions.
- Validation and error behaviour are explicit.
- Tests cover success and relevant failure/boundary cases.
- Existing tests are run and results recorded.
- No unrelated refactoring is bundled into the change.
- A review report records findings and final disposition.

## Deliverables

- Codebase map and request-flow notes.
- Baseline test record.
- One or more engineering tickets.
- Small implementation diff and regression tests.
- Code-review report and, if performed, agent-evaluation report.
- ADR only if a material design decision is required.

## Constraints

Do not claim the portfolio fork is an original application. Do not assert a defect exists until reproduced. Do not commit credentials or private data. Preserve upstream attribution and separate portfolio changes from upstream code.

## Completion evidence

Link the relevant branch/commit, test command and output, ticket, review notes and any agent report. Until those exist, keep the status Proposed or In Progress.
