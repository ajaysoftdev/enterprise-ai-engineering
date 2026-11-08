# Java Engineering

This section contains practical Java software-engineering exercises using an existing application codebase.

## Codebase

The starting codebase is the [Spring PetClinic portfolio fork](https://github.com/ajaysoftdev/spring-petclinic), based on the [canonical Spring PetClinic repository](https://github.com/spring-projects/spring-petclinic).

Spring PetClinic is an existing open-source Spring Boot sample application. The fork is used as a learning and engineering exercise base; it should not be represented as an application originally authored for this portfolio. See [third-party notices](../docs/THIRD_PARTY_NOTICES.md).

The upstream project README states that Java 17 or later is required and describes Maven Wrapper and Gradle Wrapper workflows. Confirm the current fork's build configuration before running commands.

## Featured project

[Spring PetClinic service enhancement](../projects/java-spring-petclinic/README.md)

A sequence of bounded exercises covering codebase exploration, one REST/API enhancement, validation and error handling, persistence behaviour, regression tests, code review and AI-assisted change evaluation. All changes must remain grounded in the actual upstream code and domain.

## Skills covered

- Java application development and object-oriented design
- Spring Boot, dependency injection and REST APIs
- Persistence, repositories and transaction boundaries
- Understanding request flows and existing architecture
- Debugging and root-cause analysis
- Unit, integration and API testing
- Code review, refactoring and maintainability
- AI-assisted changes and independent validation

## Planned workflow

1. Map packages, application entry point, controllers, services, repositories and entities.
2. Review build configuration, dependencies and existing tests.
3. Set up the local development environment.
4. Run the existing test suite and record a baseline.
5. Select one bounded ticket with clear acceptance criteria.
6. Implement the smallest appropriate change and add regression coverage.
7. Review the diff, run checks and record evidence.
8. Compare an AI-generated attempt with a human-reviewed solution only under documented conditions.

## Status

Project specification prepared. Local environment setup, baseline test execution and implementation exercises have not yet been completed.
