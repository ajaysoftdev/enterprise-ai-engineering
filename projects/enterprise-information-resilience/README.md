# Enterprise Information Resilience

**Purpose:** Help an enterprise detect, assess and respond to misleading, manipulated or rapidly spreading information while avoiding unnecessary escalation.

**Domain:** Digital trust, information integrity, reputation resilience and AI governance.  
**Planned stack:** Python 3.12, FastAPI, PostgreSQL, Redis and OpenTelemetry; optional provider-neutral LLM adapter.  
**Status:** Synthetic signal/case-review prototype CI + Docker verified — 6 tests passed on Python 3.12 (GitHub Actions run 42456370742, commit 23f9c4e). This verifies deterministic synthetic scoring and human-review tests only; no live monitoring or truth assessment is claimed.
**Latest revision note:** Request correlation IDs and baseline security response headers have been added; the new middleware tests are awaiting CI verification.

## Business capabilities
- Ingest signals from approved public, internal and partner sources.
- Normalise claims, entities, sources, timestamps and evidence.
- Assess source reliability, corroboration, reach, velocity and potential business impact.
- Group related signals into cases and maintain an evidence timeline.
- Route cases to communications, legal, security, risk or business owners.
- Record decisions, approvals, actions and outcomes for audit.

## Reference workflow
Signal intake → normalisation → evidence enrichment → risk assessment → case correlation → human review → approved response → outcome monitoring.

## Key modules
- **Signal intake:** connectors, source registry and ingestion validation.
- **Evidence service:** provenance, references, confidence and immutable event history.
- **Assessment engine:** configurable scoring and explainable rules.
- **Case management:** ownership, status, escalation and service-level tracking.
- **Review and response:** approval gates, response templates and action records.
- **Observability:** operational metrics, audit events and tracing.

## Expected demonstration
Use synthetic scenarios to show how multiple weak signals are correlated, prioritised and assigned for human review. Demonstrate why a case was prioritised and which evidence supported the decision.

## Guardrails
Do not automate public statements or consequential reputational decisions. Preserve source provenance, distinguish fact from allegation, support corrections and appeals, and require authorised human approval.

## First executable slice

The current prototype ingests evidence-linked synthetic signals, calculates an explainable weighted risk score, groups signals by a shared case key, adds a capped corroboration increment, supports a single human review decision and records audit events. It includes API tests, OpenAPI, SQLite persistence, Docker and GitHub Actions.

**Limitations:** signals are manually submitted and correlation uses a supplied case key; there is no web monitoring, claim extraction, entity resolution, semantic clustering, source reputation service, LLM, misinformation classifier, fact verification, legal review workflow or external response connector. Risk scores are prioritisation aids, not truth assessments. Public statements and consequential actions are not automated. GitHub Actions executed the API suite successfully: 6 passed, 0 failed. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. Synthetic evidence only.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn inforesilience.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No live monitoring, production integration or verified runtime capability is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
