"""Versioned deterministic benchmark task registry."""
TASKS = {
    "api-health-endpoint": {
        "version": "1.0",
        "description": "Add a minimal health endpoint and a corresponding test.",
        "required_files": ["src/app.py", "tests/test_app.py"],
        "required_snippets": {
            "src/app.py": ["def health_check"],
            "tests/test_app.py": ["def test_health_check"],
        },
    }
}
