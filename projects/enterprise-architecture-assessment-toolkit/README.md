# Enterprise Architecture Assessment Toolkit

**Purpose:** Turn strategy and stakeholder evidence into a structured view of business capabilities, current-state architecture, gaps, target options and a prioritised transformation roadmap.

**Domain:** Enterprise architecture, business capability assessment and technology transformation.  
**Technology direction:** Metadata-driven assessment workflows, structured architecture records, evidence links and report generation; specific implementation choices will be recorded as ADRs.  
**Status:** CI + Docker build verified — 9 tests passed on Python 3.12 (GitHub Actions run 42478891292). Authentication rejects missing/incorrect keys and fails closed when the server key is not configured. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Capture assessment scope, objectives, stakeholders and constraints.
- Model business capabilities, value streams and operating responsibilities.
- Inventory processes, information domains, applications, integrations and technology.
- Link stakeholder evidence, risks, pain points and dependencies to architecture elements.
- Identify capability gaps, duplication, obsolescence and control weaknesses.
- Compare target-state options and record trade-offs and architecture decisions.
- Generate sequenced initiatives, dependencies, owners and roadmap views.

## Reference workflow
Assessment intake → capability map → stakeholder evidence → current-state inventory → dependency and gap analysis → target options → roadmap and decisions.

## Key modules
- **Assessment workspace:** scope, stakeholders, objectives and evidence register.
- **Capability model:** capability hierarchy, maturity and business outcomes.
- **Architecture inventory:** process, data, application, integration and technology records.
- **Dependency graph:** relationships, critical paths and impact analysis.
- **Gap and option analysis:** current/target comparison, risks and trade-offs.
- **Roadmap/reporting:** initiatives, sequencing, decision log and exportable outputs.

## Expected demonstration
Assess a synthetic enterprise scenario, map a business capability to its supporting processes, data and applications, identify a duplicated integration and create a phased modernisation roadmap with explicit assumptions.

## Guardrails
Keep evidence, assumptions and recommendations distinct. Record confidence and source for assessments. Do not present generated maturity scores as objective facts without an agreed assessment method.

## First executable slice

The current prototype captures business objectives, capability maturity and evidence references; calculates current/target maturity averages; identifies capability gaps; flags duplicate and unresolved dependency relationships; prioritises gap-based roadmap initiatives; and persists assessment reports. It includes API tests, OpenAPI, Docker and GitHub Actions.

**Limitations:** maturity ratings and evidence are stakeholder-supplied and not independently verified. The roadmap uses maturity gap only; it does not yet model cost, strategic value, risk, resource capacity, transition architecture, business capability maps, application portfolios, data models or ArchiMate/TOGAF exports. Dependency findings are descriptive, not a verified graph. GitHub Actions executed the API suite successfully: 8 passed, 0 failed, including the protected-route authentication test. The latest CI run uses httpx2 and completes without the Starlette TestClient deprecation warning. No client assessment or transformation outcome is claimed.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn eatoolkit.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No client assessment, enterprise architecture certification or real-world transformation outcome is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
