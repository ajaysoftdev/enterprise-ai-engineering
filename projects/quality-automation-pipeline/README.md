# Project 5: Quality Automation Pipeline

- Status: Proposed
- Type: CI/CD and engineering-quality exercise

## Problem context

A repository needs repeatable checks so that changes are tested consistently and failures are visible before integration. The pipeline should be simple, least-privilege and truthful about what it verifies.

## Proposed scope

- Run the Java project's supported build and test command using its checked-in wrapper.
- Run Python unit tests for the data pipeline and data quality exercises.
- Validate documentation and basic repository hygiene.
- Add language-appropriate static checks where configuration is available.
- Publish test results and preserve useful failure output.
- Use minimal workflow permissions and avoid printing secrets.

## Pipeline stages

```text
Pull request / push
        |
        v
Checkout and runtime setup
        |
        +---- Java build and tests
        |
        +---- Python tests and checks
        |
        +---- Repository / documentation checks
        |
        v
Aggregate status and test evidence
```

## Acceptance criteria

- Workflow triggers are documented and appropriately scoped.
- Java and Python jobs run independently where practical.
- Runtime versions are explicit and reproducible.
- A failing test causes the corresponding job to fail.
- No credentials are hard-coded or printed.
- Workflow permissions follow least privilege.
- Dependency and static checks are clearly distinguished from tests.
- A clean pull request shows the exact checks that ran.

## Deliverables

Workflow YAML, supporting configuration, documentation of each gate and sample successful/failed run links once executed.

## Constraints

Do not add speculative gates that cannot be maintained. Do not claim a pipeline is passing until a real workflow run confirms it.
