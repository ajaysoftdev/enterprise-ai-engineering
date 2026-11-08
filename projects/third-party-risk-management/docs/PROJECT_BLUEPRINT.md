# Third-Party Risk Management — Project Blueprint

**Status:** Architecture and implementation specification

## Business problem
Manage vendor risk across onboarding, access, service delivery, monitoring, renewal and offboarding, including fourth-party dependencies.

## Reference workflow
Vendor intake → inherent risk tiering → due diligence → control/evidence assessment → approval → access review → monitoring → offboarding.

## Architecture
A task/evidence registry defines reproducible inputs; adapters isolate agents, Git and scanners; an execution controller enforces sandbox, tools, time and cost budgets; evaluators run tests and review diffs; scoring produces evidence-backed reports. For vendor risk, intake and assessment workflows maintain evidence, approvals, access and lifecycle reviews.

## Domain model
Vendor, Service, RiskTier, Assessment, Control, Evidence, Finding, Approval, AccessGrant, FourthParty, ReviewEvent. Define stable IDs, lifecycle states, evidence provenance, ownership, timestamps and retention.

## Code modules
vendor_registry, intake, tiering, questionnaire, evidence, control_assessment, approvals, access_review, monitoring, offboarding. Keep provider SDKs and external systems behind adapters. Separate policy decisions from execution and scoring.

## Interface contracts
Use versioned APIs and typed task/evidence schemas. Record correlation IDs, immutable run/evidence references, status transitions and idempotency keys.

## Security and governance
Enforce least privilege, sandbox boundaries, secret isolation, approval gates and audit. Do not execute untrusted code on the host. For vendor records, restrict access and document sensitive fields and retention.

## NFRs
Measure reproducibility, execution duration, cost, failure rate, evidence completeness and operational recovery. Define limits before evaluation claims.

## Delivery increments
1. Runnable skeleton and typed domain model.
2. Core workflow and local persistence.
3. External adapters and policy enforcement.
4. Security, observability, containers and CI.
5. Synthetic demo, evaluation report and operational runbook.

## Acceptance criteria
Clean local startup; deterministic workflow tests; explicit policy and security tests; reproducible synthetic scenario; complete evidence report; honest status labels.
