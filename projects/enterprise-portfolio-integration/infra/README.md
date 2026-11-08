# Local Infrastructure

- Python 3.11+ and SQLite for the workflow repository.
- Document Intelligence base URL configurable with DOCINT_URL (default http://localhost:8001).
- MDM base URL configurable with MDM_URL (default http://localhost:8002).
- Integration API defaults to port 8003.
- Docker Compose starts only the integration service; start the two domain services separately.
- Use synthetic supplier invoices and test-only data.
- No production secrets or customer information.
