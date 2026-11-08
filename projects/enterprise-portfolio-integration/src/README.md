# Source Layout

```text
src/portfolio_integration/
  main.py       # API and workflow orchestration
  models.py     # typed request and response contracts
  adapters.py   # HTTP adapters for Document Intelligence and MDM
  repository.py # workflow, idempotency and audit persistence
scripts/e2e_smoke.py  # real HTTP smoke test across three local services
```
