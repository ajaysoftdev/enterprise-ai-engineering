# Portfolio Security Baseline

## Purpose

This baseline defines minimum engineering controls for the 16 synthetic portfolio projects. It is a development standard, not a claim of security certification or production readiness.

## Current automated checks

The `.github/workflows/portfolio-security.yml` workflow runs, for each project:

- Bandit static analysis over `src/`.
- `pip-audit --skip-editable` against resolved third-party dependencies (editable local project packages are excluded from the PyPI vulnerability lookup).
- A Python 3.12 environment and the project's declared development dependencies.
- Weekly dependency update PRs are configured through `.github/dependabot.yml` for all 15 Python projects and GitHub Actions.

A green run means only that these two automated checks completed for the scanned commit. It does not prove the absence of vulnerabilities or replace threat modelling, code review, penetration testing, container scanning or runtime controls.

## Implemented baseline in the current prototype revision

All 15 FastAPI services now attach a bounded `X-Request-ID` correlation value (accepting only 1–64 safe characters or generating a random replacement) and return `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer` and `Cache-Control: no-store`. New tests cover valid and malformed request IDs. These controls improve traceability and response hygiene; they do not provide authentication, authorization, tenant isolation or rate limiting. CI verification of this revision is pending.

## Minimum API and service controls before external exposure

1. **Identity:** authenticate every non-health endpoint using an enterprise identity provider or a short-lived service credential.
2. **Authorization:** enforce tenant, resource and action-level authorization on the server; do not trust caller-supplied actor or tenant identifiers.
3. **Secrets:** load secrets from a managed secret store; never commit credentials or use static production secrets in environment examples.
4. **Transport:** require TLS at the ingress and service-to-service boundaries; use mTLS where workload identity and risk warrant it.
5. **Input handling:** validate schema, size, encoding, content type and file signatures; treat all external text, files, events and model output as untrusted.
6. **Abuse resistance:** apply rate limits, request timeouts, payload limits, pagination limits and bounded concurrency.
7. **Persistence:** use parameterised queries, least-privilege database identities, encryption at rest, backup/restore tests and migration controls.
8. **Audit:** record actor identity, action, target, timestamp, correlation ID and decision rationale; protect audit storage against alteration and restrict read access.
9. **Privacy:** minimise collected data, redact sensitive values from logs, define retention/deletion policies and use synthetic fixtures in public demos.
10. **AI-specific controls:** isolate tools, constrain permissions, validate outputs, defend against prompt injection and require human approval for consequential operations.
11. **Supply chain:** pin and review dependencies, scan source and containers, generate an SBOM, verify build provenance and review third-party actions.
12. **Operations:** expose readiness/liveness, structured logs, metrics and traces; define incident response, recovery objectives and ownership.

## Project-specific safety boundaries

- Document intelligence: no untrusted file parsing until malware scanning, quarantine, content limits and parser isolation exist.
- Information resilience: a risk score is not a truth verdict; no automatic publication, takedown or external response.
- Breach resilience: attack-path and containment actions are simulations; no live identity or endpoint control.
- Data protection: masking examples do not replace a formal classification policy or cryptographic key management.
- MDM: matching suggestions require stewardship; no irreversible merge or deletion by an automated match.
- Agent operations and AI workbench: no unrestricted shell, network, credential or production-system access.
- Integration: retries must be bounded; idempotency, replay and dead-letter access require explicit operational controls.
- Life sciences and pharma: synthetic examples only; no GxP, validated-system or regulated-data claims.
- SAP modernisation: no live SAP connection or migration execution.
- Third-party risk: synthetic evidence and scores do not constitute an audit or supplier certification.
- EA assessment: maturity scores are decision support, not independent assurance or a validated target-state design.

## Release evidence required before calling a prototype production-ready

- Threat model and abuse cases reviewed.
- Authentication, authorization and tenant-isolation tests passed.
- SAST, dependency, secret, container and IaC scans reviewed with no unresolved critical/high findings.
- Contract, integration, negative-path, concurrency and recovery tests passed.
- Backup/restore and disaster-recovery exercises recorded.
- Operational dashboards, alerts, runbooks and ownership defined.
- Privacy, retention, data residency and regulatory obligations assessed by the accountable organisation.
- Independent security review and deployment approval completed.

## Current status

- Bandit static analysis completed successfully for all 15 projects in the initial portfolio scan.
- The first dependency audit identified a known vulnerability in the previously pinned `pytest 8.4.2` release (fixed upstream in `9.0.3`). All 15 projects have been updated to `pytest>=9.0.3,<10.0`.
- The audit command now uses `pip-audit --skip-editable` so the locally installed portfolio package is not incorrectly looked up as a published PyPI dependency.
- The clean security matrix completed successfully for the **15 core projects**: 15/15 jobs passed Bandit and pip-audit in GitHub Actions run 42461092337 (Dependabot workflow-update branch, based on main commit 5fd42f7). The sixteenth Enterprise Portfolio Integration project was added afterward; its security scan is pending.
- Request correlation middleware and its tests have been added across all 15 core APIs and passed in CI. The integration project has the same request-context controls; its security scan is pending.

Existing test and Docker evidence remains limited to the exact synthetic prototype revisions described in each project README.
