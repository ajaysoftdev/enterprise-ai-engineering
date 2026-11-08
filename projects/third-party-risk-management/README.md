# Third-Party Risk Management

**Purpose:** Manage vendor risk consistently across onboarding, due diligence, access, service delivery, renewal, monitoring and offboarding.

**Domain:** Third-party cyber risk, supplier governance and operational resilience.  
**Technology direction:** Workflow/API services, evidence metadata, risk rules and audit records; specific implementation choices will be captured in ADRs.  
**Status:** CI + Docker build verified — 9 tests passed on Python 3.12 (GitHub Actions run 42478881646). Authentication rejects missing/incorrect keys and fails closed when the server key is not configured. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Maintain vendor, service, contract and fourth-party dependency records.
- Assess inherent risk based on service criticality, data access and exposure.
- Collect due-diligence questionnaires, attestations and control evidence.
- Track findings, remediation plans, exceptions and approval decisions.
- Govern vendor identities, access grants and periodic recertification.
- Monitor changes, incidents, renewals and offboarding obligations.

## Reference workflow
Vendor intake → inherent risk tiering → due diligence → control/evidence assessment → approval → access review → continuous monitoring → renewal or offboarding.

## Key modules
- **Vendor registry:** vendor, service, owner, contract and dependency data.
- **Risk assessment:** tiering, questionnaires and configurable scoring.
- **Evidence management:** document metadata, validity and control mapping.
- **Findings and remediation:** issue ownership, due dates and exceptions.
- **Access governance:** access inventory, approval and revocation tracking.
- **Monitoring:** reassessment triggers, incidents and renewal workflow.

## Expected demonstration
Onboard a synthetic SaaS provider, classify its risk based on data and service criticality, record evidence gaps, assign remediation and demonstrate access review before renewal.

## Guardrails
Protect confidential vendor evidence, restrict access by role and record evidence freshness. Risk scores support accountable decisions; they do not replace contractual, legal or security review.

## First executable slice

The current prototype registers synthetic vendors, calculates explainable inherent-risk scores and HIGH/MEDIUM/LOW tiers, defines tier-specific due-diligence controls, tracks evidence validity dates and blocks approval until required evidence is current. It includes API tests, OpenAPI, SQLite persistence, Docker and a GitHub Actions workflow.

**Limitations:** risk weights and required controls are illustrative. There are no vendor questionnaire integrations, document storage/scanning, external risk feeds, fourth-party graph, access inventory, identity provider, contract lifecycle, continuous monitoring, role-based approval authority or regulatory/legal review. Evidence references are metadata only; evidence files are not verified. GitHub Actions executed the API suite successfully: 8 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. Synthetic vendors only.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn tprm.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No real vendor assessment, certification or external supplier connection is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
