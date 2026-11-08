# Reference sources — Enterprise Document Intelligence

These resources are design and implementation references. The project should use synthetic documents until security, privacy and retention controls are implemented.

## Document processing and extraction
- [SAP Document Processing Reference Architecture](https://architecture.learning.sap.com/docs/ref-arch/744df4) — multi-channel intake, extraction, enrichment, confidence routing and downstream posting patterns.
- [Azure AI Document Intelligence documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/overview) — OCR, layout and structured document extraction concepts.
- [AWS Textract documentation](https://docs.aws.amazon.com/textract/) — OCR and document-analysis API patterns.
- [Tesseract OCR documentation](https://tesseract-ocr.github.io/) — open-source OCR option for local experiments.

## Application and governance
- [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://docs.pydantic.dev/latest/) — typed API contracts and validation.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — evaluation, monitoring and human oversight.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — prompt injection and unsafe output handling.
- [OpenTelemetry](https://opentelemetry.io/docs/) — end-to-end traceability.

## Apply these references to this project
Keep OCR and model providers behind replaceable adapters; retain page/region evidence for extracted fields; validate against deterministic business rules; route low-confidence or high-impact fields to a human; record corrections and model/version metadata. Do not treat an extraction confidence score as proof of correctness.
