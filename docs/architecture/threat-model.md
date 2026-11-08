# Threat Model Method

- Status: Reusable method, not a completed project assessment
- Approach: STRIDE-inspired discovery

## 1. Assets
Source code, repository credentials, build artifacts, configuration, secrets, business/test data, APIs, event messages, CI runners and AI-agent tool permissions.

## 2. Trust boundaries
Browser-to-service, service-to-service, application-to-database, producer-to-broker, CI-to-repository and agent-to-tool boundaries.

## 3. Threat categories

| Category | Example | Candidate controls |
|---|---|---|
| Spoofing | Stolen service identity | Strong authentication, short-lived credentials |
| Tampering | Modified event or build artifact | Integrity validation, signatures, audit |
| Repudiation | Untraceable replay | Correlation IDs and audit events |
| Disclosure | Secret/PII in logs | Redaction and minimisation |
| Denial of service | Oversized upload/retry storm | Limits, quotas and backpressure |
| Elevation | Over-permissive CI token | Least privilege and approvals |

## 4. AI-specific risks
Prompt injection through repository content, secret disclosure, unsafe generated code, destructive tool actions and false claims about tests. Mitigate with constrained tools, isolated branches, secret-free environments, diff review and independent checks.

## 5. Risk record
For each threat record asset, attack path, likelihood, impact, existing control, residual risk, evidence, owner role and target action. Use Low/Medium/High unless a defined scoring model exists.

## 6. Required outputs
Context/data-flow diagram, asset inventory, trust boundaries, threat register, mitigation/verification plan and residual-risk review.

## 7. Completion rule
A threat assessment is complete only when scoped to a specific project version and reviewed. This method is not a penetration test.
