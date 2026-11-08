# Enterprise Document Intelligence

**Purpose:** Convert business documents into validated, traceable information and route uncertain cases to the right human reviewer.

**Domain:** Document AI, workflow automation and controlled business inference.  
**Planned stack:** Python 3.12, FastAPI, Pydantic, PostgreSQL, OCR and LLM adapters.  
**Status:** Architecture specification documented. Executable implementation, automated test runs and deployment verification are pending.

## Business capabilities
- Receive invoices, claims, contracts, forms and operational documents.
- Classify document type and extract typed fields with page-level evidence.
- Validate extracted values against schemas, business rules and reference data.
- Detect missing fields, conflicts, duplicates and low-confidence results.
- Route exceptions to role-based human review with correction history.
- Publish approved structured records through APIs or downstream adapters.

## Reference workflow
Document intake → file validation → classification/OCR → field extraction → evidence linking → business validation → confidence and exception routing → human approval → downstream publication.

## Key modules
- **Intake:** upload/API adapters, file checks and document registry.
- **Extraction:** OCR abstraction, layout parsing and model/provider adapters.
- **Validation:** Pydantic schemas, deterministic rules and reference lookups.
- **Review:** field-level evidence, correction, approval and rejection.
- **Publication:** versioned output contract and idempotent delivery.
- **Audit:** document lineage, model/version trace and reviewer actions.

## Expected demonstration
Process synthetic invoices and contracts, show extracted fields with source-page evidence, deliberately introduce missing or inconsistent values, and demonstrate human correction before publication.

## Guardrails
Treat extracted content as untrusted input. Do not execute embedded instructions. Keep model output separate from verified facts, protect document contents, and require approval for material financial or contractual actions.

## Project documentation
- [Detailed blueprint](docs/PROJECT_BLUEPRINT.md)
- [Source-code boundaries](src/README.md)
- [Test strategy](tests/README.md)
- [Local deployment and operations](infra/README.md)

## Delivery status
The documents define the intended design and acceptance criteria. No production OCR accuracy, customer integration or runtime test result is claimed.