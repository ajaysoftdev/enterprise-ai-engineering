# Enterprise Data Protection

**Purpose:** Make enterprise data handling consistent and auditable from discovery and classification through access, use, sharing and retention.

**Domain:** Data protection, privacy engineering and information governance.  
**Planned stack:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, policy adapter and synthetic data.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No regulatory certification, production data processing or deployed privacy control is claimed.

## Reference sources

See [SOURCES.md](SOURCES.md) for curated official documentation, standards, reference architectures and implementation resources, with notes on how each applies to this project.
