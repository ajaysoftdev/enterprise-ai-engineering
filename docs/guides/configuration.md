# Configuration Management

## Principles
- Keep environment-specific values outside source code.
- Separate ordinary settings from secrets.
- Provide safe examples with placeholders.
- Validate required settings at startup.
- Document defaults, allowed values and operational impact.

| Setting | Example | Handling |
|---|---|---|
| Runtime version | Java 17+ | Document per project |
| Active profile | local / test | Non-secret setting |
| Database URL | local H2/test DB | Environment-specific |
| Database credentials | Placeholder only | Secret store or ignored local file |
| External endpoint | Local test URL | Validate destination |
| Log level | INFO | Avoid verbose production logs |

Exact property names must come from each project's current configuration; this is not a complete property inventory.

## Local overrides
Use environment variables or ignored local files. Never edit committed defaults to add passwords. Keep checked-in examples fake.

## Validation and change control
Validate URL formats, numeric bounds, profile names and incompatible settings. For every change record purpose, affected environments, secret impact, rollback and test evidence.

Never put secrets in command-line arguments, screenshots, issue descriptions or reports.
