# Reference sources — Enterprise Attention and Intelligence Hub

## Observability and reliability
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — vendor-neutral traces, metrics and logs.
- [Prometheus documentation](https://prometheus.io/docs/introduction/overview/) — metrics collection and alerting model.
- [Google SRE books](https://sre.google/books/) — service-level objectives, alert quality and operational reliability.
- [OpenMetrics specification](https://openmetrics.io/) — metrics exposition format.

## Event and service context
- [CloudEvents specification](https://cloudevents.io/) — common event envelope.
- [OpenAPI specification](https://spec.openapis.org/oas/latest.html) — API contracts for signal and work-item services.
- [CNCF TAG Observability](https://github.com/cncf/tag-observability) — observability practices and ecosystem guidance.

## Apply these references to this project
Correlate signals with service ownership, dependency and business capability; avoid alerting on every raw metric. Define SLOs and alert thresholds with operational owners. Preserve source links and explainable impact factors; measure noise reduction and action outcomes rather than counting dashboards.
