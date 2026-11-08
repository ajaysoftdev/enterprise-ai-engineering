# Enterprise Architecture Assessment Toolkit

**Purpose:** Turn strategy and stakeholder evidence into a structured view of business capabilities, current-state architecture, gaps, target options and a prioritised transformation roadmap.

**Domain:** Enterprise architecture, business capability assessment and technology transformation.  
**Technology direction:** Metadata-driven assessment workflows, structured architecture records, evidence links and report generation; specific implementation choices will be recorded as ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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
