# Reference sources — Cloud Data Engineering Platform

## Lakehouse and table formats
- [Databricks medallion architecture](https://docs.databricks.com/en/lakehouse/medallion.html) — raw, refined and curated data-zone pattern.
- [Delta Lake documentation](https://docs.delta.io/) — transactional table and incremental processing concepts.
- [Apache Iceberg documentation](https://iceberg.apache.org/docs/latest/) — open table format and schema/partition evolution.

## Engineering, orchestration and quality
- [Apache Airflow documentation](https://airflow.apache.org/docs/) — workflow orchestration patterns.
- [dbt documentation](https://docs.getdbt.com/) — SQL transformation, testing and documentation.
- [Great Expectations](https://docs.greatexpectations.io/) — data-quality validation.
- [OpenLineage](https://openlineage.io/docs/) — interoperable pipeline and dataset lineage.
- [OpenTelemetry](https://opentelemetry.io/docs/) — pipeline service telemetry.

## Apply these references to this project
Keep storage formats and cloud providers behind adapters. Define contracts at ingestion, idempotent incremental loads, schema evolution, quarantine, replay, lineage and cost attribution. Treat bronze/silver/gold as a logical pattern, not a mandatory vendor-specific implementation.
