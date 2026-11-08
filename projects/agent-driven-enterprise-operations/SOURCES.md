# Reference sources — Agent-Driven Enterprise Operations

## Agent interoperability and tool access
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) — standardised context and tool-server interaction.
- [A2A Protocol](https://a2a-protocol.org/latest/specification/) — agent-to-agent discovery and collaboration concepts.
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/) — agent orchestration, tools, handoffs and tracing implementation reference.

## Governance and safety
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — govern, map, measure and manage AI risks.
- [OWASP Top 10 for Agentic Applications](https://owasp.org/www-project-top-10-for-agentic-applications/) — agent-specific threat patterns.
- [Open Policy Agent](https://www.openpolicyagent.org/docs/latest/) — externalised authorisation and policy decisions.
- [Temporal documentation](https://docs.temporal.io/) — durable workflow execution and recovery patterns.

## Apply these references to this project
Treat every tool as a privileged API. Give agents narrow, expiring permissions; validate inputs and outputs; enforce budgets and step limits; persist workflow state; require approval for payments, access changes, external communications or destructive actions. Log tool arguments/results with sensitive data redacted.
