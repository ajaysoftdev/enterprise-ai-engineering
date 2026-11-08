# Data Model and Data Quality Reference

- Status: Proposed portfolio reference
- Related: [Python pipeline](../../projects/python-batch-data-pipeline/README.md), [Data quality](../../projects/data-quality-framework/README.md)

## 1. Conceptual entities

| Entity | Key | Relationship |
|---|---|---|
| Customer | customer_id | One customer places many orders |
| Order | order_id | Belongs to customer; contains lines |
| OrderLine | order_line_id | Belongs to order; references product |
| Product | product_id | Appears on order lines |
| SourceRecord | source_record_id | Tracks file, row and batch |
| QualityIssue | issue_id | Identifies rejected row and rule |

## 2. Canonical fields

| Field | Type | Required | Rule |
|---|---|---:|---|
| customer_id | string | Yes | Stable non-empty identifier |
| email | string | No | Validate format; classify as personal data |
| order_id | string | Yes | Unique within source scope |
| order_date | ISO 8601 | Yes | Parseable and in allowed range |
| currency | string | Yes | Supported currency code |
| product_id | string | Yes | Resolves to product master |
| quantity | positive integer | Yes | Greater than zero |
| unit_price | decimal | Yes | Non-negative; avoid binary float for currency |
| source_system | string | Yes | Controlled identifier |
| batch_id | string | Yes | Identifies ingestion run |

## 3. Data flow
Source files -> immutable raw input -> schema mapping -> profiling/validation -> accepted canonical records; rejected rows are retained with issue reasons.

## 4. Quality dimensions
Completeness, validity, uniqueness, consistency, referential integrity and timeliness. Each rule needs an ID, severity, scope, expression, threshold and owner.

## 5. Lineage and reconciliation
Record source file, row number, batch, transformation version and output identifier. Reconcile input rows to accepted, rejected, duplicate and explicitly skipped counts.

## 6. Privacy
Use synthetic data. If personal data is introduced, minimise fields, restrict access, mask examples and define retention/deletion before processing.

## 7. Acceptance
Version the canonical schema, trace every rejection to a rule, reconcile batch counts, make reruns deterministic and retain source-to-output lineage.
