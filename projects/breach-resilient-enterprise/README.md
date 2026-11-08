# Breach-Resilient Enterprise

**Purpose:** Model how an enterprise contains an assumed compromise across identity, applications, data, APIs and software delivery.

**Domain:** Zero-trust security architecture, attack-path containment and cyber resilience.  
**Planned stack:** Python 3.12, FastAPI, OPA/Rego policy examples, Docker Compose and OpenTelemetry.  
**Status:** CI + Docker build verified — 9 tests passed on Python 3.12 (GitHub Actions run 42478821593). Authentication rejects missing/incorrect keys and fails closed when the server key is not configured. This verifies synthetic/local prototype behaviour only, not production readiness.
**Latest revision verified:** Request correlation IDs, malformed-ID replacement and baseline security response headers passed in the latest CI run.

## Business capabilities
- Represent identities, workloads, resources, trust boundaries and access paths.
- Evaluate least-privilege and contextual access policies.
- Map attack paths and identify excessive privilege or exposed trust relationships.
- Demonstrate segmentation, credential containment and secret rotation workflows.
- Correlate security signals with affected services and business impact.
- Track response, recovery and evidence for audit.

## Reference workflow
Asset and identity inventory → trust-boundary mapping → policy evaluation → attack-path analysis → detection → containment approval/action → recovery validation → evidence reporting.

## Key modules
- **Identity and access:** principals, roles, workload identities and privilege scope.
- **Policy engine:** policy-as-code examples and explainable decisions.
- **Exposure graph:** relationships among identities, workloads, APIs and data.
- **Detection and response:** event normalisation, incident state and response playbooks.
- **Recovery:** credential rotation, restore checks and recovery evidence.
- **Telemetry:** security events, audit trail and service-level observability.

## Expected demonstration
Use a synthetic enterprise topology to simulate a compromised identity, trace reachable resources, identify excessive access and demonstrate a controlled containment workflow.

## Guardrails
This is a defensive engineering project. Use isolated synthetic environments only. Never include real credentials, exploit third-party systems or represent a simulated control as a deployed security capability.

## First executable slice

The current prototype includes a FastAPI service, a synthetic identity/workload/resource graph, deterministic attack-path traversal, default-deny policy evaluation, human-gated containment planning, an OpenAPI contract, synthetic topology fixture, API tests, Dockerfile and GitHub Actions workflow.

**Limitations:** the topology is hard-coded in Python and represents synthetic examples only. Policy evaluation is a simplified demonstration, not an enterprise policy engine. Containment is always simulation-only; no identity provider, cloud, network, endpoint, secrets or SOC control is connected. Authentication, authorisation, tenant isolation, persistence, real event ingestion, telemetry, OPA/Rego integration and security testing remain pending. Tests have been added but have not yet been executed in CI. This is not a deployed security control.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn breach.main:app --reload --app-dir src
pytest
```

Docker: `docker compose up --build`. API contract: [openapi.yaml](openapi.yaml). Synthetic graph: [examples/synthetic-topology.json](examples/synthetic-topology.json).

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No enterprise security certification, live SOC integration or production protection is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.

## Implementation architecture

See [IMPLEMENTATION_ARCHITECTURE.md](IMPLEMENTATION_ARCHITECTURE.md) for the proposed logical architecture, workflow, API/event contracts, data model, security, operational requirements, acceptance tests and delivery sequence.

## Domain contracts and data model

See [DOMAIN_CONTRACTS.md](DOMAIN_CONTRACTS.md) for proposed domain entities, REST endpoints, event names, workflow, invariants and contract-test scenarios.


## Local API authentication

All application endpoints except `/health` require an API key. Copy `.env.example` to `.env`, replace the placeholder with a long random secret, then start the container with `docker compose up --build`. Docker Compose passes `API_KEY` into the service. For direct local execution, set `API_KEY` in the shell before starting Uvicorn. Never commit the populated `.env` file. CI uses a disposable test-only key.
