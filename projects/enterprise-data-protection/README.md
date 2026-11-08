# Enterprise Data Protection

**Purpose:** Make enterprise data handling consistent and auditable from discovery and classification through access, use, sharing and retention.

**Domain:** Data protection, privacy engineering and information governance.  
**Planned stack:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, policy adapter and synthetic data.  
**Status:** CI + Docker build verified — 9 tests passed on Python 3.12 (GitHub Actions run 42477937900, commit fee9bb2). Authentication is enforced for protected API routes; the test suite includes a missing-key rejection check. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Discover and register datasets, fields, owners and processing purposes.
- Classify sensitive data and record handling requirements.
- Apply minimisation, masking, tokenisation and retention rules.
- Evaluate user, service and purpose-based access requests.
- Track lineage, policy decisions, exceptions and audit evidence.
- Support controlled data sharing and periodic access review.

## Reference workflow
Dataset registration → discovery and classification → purpose and risk assessment → policy assignment → access or transformation request → policy evaluation → approved processing → audit and retention review.

## Key modules
- **Data catalogue:** dataset and field metadata, ownership and lineage.
- **Classification:** rules and labels for personal, financial and confidential data.
- **Protection:** masking, tokenisation and minimisation adapters.
- **Policy decision:** purpose, role, attribute and environment checks.
- **Access governance:** approvals, expiry and recertification.
- **Audit:** policy outcomes, exceptions and evidence records.

## Expected demonstration
Register synthetic customer and transaction datasets, classify sensitive fields, apply masking profiles, evaluate role/purpose access and inspect the audit history.

## Guardrails
Use synthetic data. Keep keys and secrets outside source control. Separate policy administration from policy enforcement and ensure denied access, exceptions and overrides are auditable.

## First executable slice

The current prototype includes dataset registration with field-level classifications, a SQLite metadata store, purpose/role/classification-aware access evaluation, deterministic masking, policy-decision audit records, API tests, OpenAPI, Docker and a GitHub Actions workflow.

**Limitations:** policy rules are illustrative and hard-coded; no identity provider, attribute-based access engine, external catalogue, token vault, encryption/key management, lineage integration, retention scheduler or tenant isolation is connected. The masking examples are deterministic transformations, not anonymisation guarantees. Authentication, authorization enforcement at a data gateway, concurrency testing and security assessment remain pending. GitHub Actions executed the API suite successfully: 9 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. Do not use real personal or financial data.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn dataprotection.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No regulatory certification, production data processing or deployed privacy control is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
