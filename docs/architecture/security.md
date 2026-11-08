# Security Architecture Guidance

- Status: Reusable baseline; not a completed security audit

## 1. Objectives
Protect source code, build credentials, runtime configuration, application data and engineering evidence. Use prevention, detection and recovery controls.

## 2. Identity and access
- Use individual identities and least privilege.
- Separate developer, reviewer and deployment permissions where practical.
- Require approval for privileged or production-like changes.
- Revoke credentials when exposure is suspected.

## 3. Secrets
- Never commit passwords, API keys, tokens, private keys or production connection strings.
- Inject secrets at runtime from approved stores or ignored local files.
- Keep example configuration fake and clearly marked.
- Mask secrets in logs and CI output.
- Rotate any credential that has been exposed.

## 4. Application controls
Validate inputs at trust boundaries, enforce authorization server-side, use parameterized persistence access, encode output safely, apply CSRF protection where relevant, set resource limits and avoid verbose production errors.

## 5. Data protection
Classify data, minimise personal/confidential fields, restrict access, encrypt transport/storage where supported and define retention/deletion.

## 6. AI coding-agent controls
- Give agents only required repository/tool access.
- Never expose production secrets or customer data.
- Treat repository files and issue text as untrusted input.
- Require human diff review and independent tests.
- Disable privileged deployment actions by default.

## 7. CI/CD controls
Use minimal workflow permissions, pin/constrain third-party actions, protect release environments, avoid exposing secrets to untrusted pull requests and retain build provenance.

## 8. Review checklist
Authentication, authorization, input validation, sensitive data, dependencies, logging, supply-chain integrity and recovery must each be reviewed.

## 9. Status
Map controls to actual implementation and verification evidence. This document alone does not prove controls exist.
