# Test Strategy

- Health and request-context headers.
- Successful document-to-MDM workflow.
- Missing extracted supplier identity pauses for review.
- Idempotency: same key/same payload and same key/different payload.
- MDM match candidate requires stewardship.
- Refresh after confirmed/rejected stewardship.
- Downstream unavailable and malformed responses.
- Workflow audit and invalid state transitions.

Only synthetic data is permitted. Record actual CI run, Python version, command, test count and failures.
