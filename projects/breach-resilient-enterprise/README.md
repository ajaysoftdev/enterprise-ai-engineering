# Breach-Resilient Enterprise

**Domain:** Zero-trust security architecture and attack-path containment  
**Status:** Architecture specification; implementation and runtime verification pending.

## Start here
- [Project blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code structure and implementation boundaries](src/README.md)
- [Test strategy and definition of done](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Planned repository layout
```text
breach-resilient-enterprise/
├── docs/
│   ├── PROJECT_BLUEPRINT.md
│   └── adr/
├── src/
│   ├── app/
│   ├── api/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── observability/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
├── infra/
│   ├── Dockerfile
│   ├── compose.yaml
│   └── deploy/
├── scripts/
├── .github/workflows/
├── .env.example
├── pyproject.toml
└── README.md
```

The layout is a target structure. Directories and executable modules will be added with implementation increments; empty directories are not represented as committed Git objects.

## Engineering status
- Architecture and module boundaries: documented.
- Executable application: pending.
- Automated tests: planned; not yet run.
- Container/CI verification: pending.
- Production deployment: not claimed.

See [project blueprint](docs/PROJECT_BLUEPRINT.md) for business flow, domain model, interfaces, security, NFRs, delivery increments and acceptance criteria.
