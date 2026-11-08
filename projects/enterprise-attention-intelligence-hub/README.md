# Enterprise Attention and Intelligence Hub

**Purpose:** Reduce operational alert and KPI overload by translating technical signals into prioritised business decisions and accountable actions.

**Domain:** Business-impact observability, event correlation and decision prioritisation.  
**Planned stack:** Python 3.12, FastAPI, PostgreSQL, Redis, event adapters and OpenTelemetry.  
**Status:** First executable prototype added — CI execution pending.

## Business capabilities
- Ingest alerts, service metrics, business KPIs and operational events.
- Correlate related signals across applications and business capabilities.
- Enrich signals with service ownership, dependency and business-impact context.
- Prioritise incidents using explainable severity and urgency rules.
- Route decisions to accountable teams with acknowledgement and escalation.
- Track time to acknowledge, resolve and restore business service.

## Reference workflow
Signal ingestion → normalisation → entity and service enrichment → correlation → impact assessment → priority calculation → action routing → acknowledgement and resolution tracking.

## Key modules
- **Signal adapters:** alert, metric, event and business KPI ingestion.
- **Context graph:** services, owners, dependencies and business capabilities.
- **Correlation:** grouping, deduplication and temporal relationships.
- **Prioritisation:** explainable impact, urgency and confidence.
- **Action management:** assignment, escalation and status tracking.
- **Analytics:** operational trends and attention/decision effectiveness.

## Expected demonstration
Feed synthetic infrastructure and business events, correlate multiple alerts into one service-impact case, explain its priority and route it to an accountable owner.

## Guardrails
Avoid opaque priority scores. Preserve original signals, explain correlations and allow authorised operators to override or correct recommendations.

## First executable slice

The current prototype provides signal ingestion, SQLite persistence, a deterministic weighted impact score, P1–P4 priority bands, correlation-key grouping, an explanation of score factors and operator acknowledgement. It includes API tests, OpenAPI, Docker and a GitHub Actions workflow.

**Limitations:** signals are synthetic/manual API submissions; there are no Prometheus, OpenTelemetry, cloud-monitoring or ticketing connectors, service dependency graph, time-window correlation, SLO evaluation, escalation scheduler, role-based access control or multi-tenant controls. The scoring weights are illustrative and require business-owner calibration. No incident reduction or operational performance claim is made. Tests have been added but have not yet been executed in CI.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn attention.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No live monitoring platform, measured incident reduction or production integration is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.
