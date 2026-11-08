# Enterprise Attention and Intelligence Hub

**Purpose:** Reduce operational alert and KPI overload by translating technical signals into prioritised business decisions and accountable actions.

**Domain:** Business-impact observability, event correlation and decision prioritisation.  
**Planned stack:** Python 3.12, FastAPI, PostgreSQL, Redis, event adapters and OpenTelemetry.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No live monitoring platform, measured incident reduction or production integration is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.
