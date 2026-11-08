# Local Engineering Quickstart

## 1. Common tools
Git, an editor, a supported JDK for Java work and Python for Python work. Docker is optional unless a task requires a database/container. Obtain installers from official vendor/project sources.

## 2. Java / Spring PetClinic
The current PetClinic Maven build sets Java 17 and the repository includes Maven and Gradle wrapper scripts. A global Maven installation is not initially required.

Windows PowerShell:
    java -version
    .\mvnw.cmd -version
    .\mvnw.cmd test

Start:
    .\mvnw.cmd spring-boot:run

Open http://localhost:8080. Upstream documentation describes H2 as the default local database.

If Java is missing, install a JDK 17 distribution, reopen the terminal and verify java -version. Do not mark the baseline passed until commands complete successfully.

## 3. Python
Check python --version. Create an isolated environment with:
    python -m venv .venv
Install only dependencies declared by the project.

## 4. Baseline record
Record OS/runtime versions, branch, starting commit, exact command, exit code and concise output. Do not commit machine identifiers, personal data or secrets.

## 5. Safe workflow
Use a feature branch, inspect the diff and keep local secrets and generated artifacts out of source control.
