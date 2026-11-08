# Testing and Quality Guide

## 1. Test levels

| Level | Purpose | Example |
|---|---|---|
| Unit | Isolated logic | Validation and transformation |
| Slice | Framework boundary | MVC or repository slice |
| Integration | Multiple components | JPA with test database |
| End-to-end | User journey | Browser workflow |
| Contract | Interface compatibility | JSON schema / API contract |
| Non-functional | Performance/resilience | Load or failure test |

## 2. Java
PetClinic includes Maven and Gradle build definitions, Java version enforcement, formatting and Checkstyle validation in Maven, JaCoCo configuration and tests for web, validation and persistence. Confirm exact commands and outcomes in the current repository.

    ./mvnw test
    ./mvnw verify

Windows PowerShell uses .\mvnw.cmd.

## 3. Python
Test parsing, schema validation, transformation, idempotency, malformed/empty input, duplicate handling and output reconciliation with synthetic fixtures.

## 4. AI-generated changes
Capture starting commit, task, agent configuration and diff. Inspect every change, run tests independently, add missing edge-case tests and record human intervention. Agent statements are not test evidence.

## 5. Evidence
Record commit, environment, command, timestamp, exit status, test count and failures. Use Passed, Failed, Blocked and Not Run distinctly.

## 6. Review gate
Acceptance criteria, relevant test evidence, understood static-check findings, clean diff and documented limitations are required before a change is considered ready.
