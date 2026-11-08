# Troubleshooting Guide

## General method
1. Capture exact command and error.
2. Confirm branch and working-tree state.
3. Check runtime/dependency versions.
4. Reproduce with the smallest input or test.
5. Inspect the first causal error.
6. Change one variable at a time.
7. Add a regression test for confirmed code defects.
8. Record resolution and uncertainty.

## Java / Maven

| Symptom | Checks |
|---|---|
| java not found | Install JDK 17+, reopen terminal, check PATH/JAVA_HOME |
| Wrapper fails | Check wrapper files, network and Java |
| Version rejected | Compare installed JDK with java.version in pom.xml |
| Dependency resolution fails | Check network/proxy and Maven repository |
| Formatting/Checkstyle fails | Read first reported file/rule |
| Test failure | Re-run smallest failing test and inspect first causal error |
| Port conflict | Identify process using port 8080 |

## Database profiles
Confirm active Spring profile, service health, port, database name and credentials. PetClinic has H2 default settings and separate MySQL/PostgreSQL profiles.

## Python pipeline
Check encoding, delimiter, headers, schema version, date/number conversion, duplicate scope and rejected output. Preserve input for reproducibility.

## CI
Compare local and CI runtime versions, variables, permissions, line endings, network dependencies and test data.

## Credential exposure
Revoke/rotate immediately, assess access logs and follow provider incident procedure. Deleting a secret from the latest commit does not invalidate it.
