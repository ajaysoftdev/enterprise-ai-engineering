# Contributing

## Before changing code

1. Read the relevant project README, implementation architecture and domain contracts.
2. Confirm the project scope and identify assumptions.
3. Use synthetic data only. Do not commit credentials, customer records, private source code or production exports.
4. Keep provider-specific code behind adapters and preserve explicit domain boundaries.

## Required checks

For a Python project:

```bash
python -m pip install -e ".[dev]"
pytest -q
bandit -q -r src
pip-audit --skip-editable
docker build -t project-name:local .
```

Run commands from the relevant project directory. Report commands that could not be executed; never describe a planned check as passed.

## Pull request expectations

- Explain the business problem and bounded scope.
- Identify API, event, data-model and architecture changes.
- Include tests for success, validation, authorization, failure and state-transition paths as applicable.
- Explain migration, retry, idempotency and rollback effects where relevant.
- Document security, privacy and AI-specific risks.
- Update the README, OpenAPI/domain contracts, implementation architecture and ADRs when affected.
- State exactly what was implemented, simulated, tested and not tested.

## Design principles

- Prefer small, reviewable changes and deterministic business rules.
- Treat all external input and model output as untrusted.
- Keep consequential actions behind authorization and human approval.
- Do not introduce real external integrations without an explicit adapter contract and safe test environment.
- Avoid claiming production readiness, compliance or security assurance from unit tests alone.
