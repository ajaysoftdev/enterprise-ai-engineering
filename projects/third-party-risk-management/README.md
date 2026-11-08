# Third-Party Risk Management

**Purpose:** Manage vendor risk consistently across onboarding, due diligence, access, service delivery, renewal, monitoring and offboarding.

**Domain:** Third-party cyber risk, supplier governance and operational resilience.  
**Technology direction:** Workflow/API services, evidence metadata, risk rules and audit records; specific implementation choices will be captured in ADRs.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

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

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No real vendor assessment, certification or external supplier connection is claimed.