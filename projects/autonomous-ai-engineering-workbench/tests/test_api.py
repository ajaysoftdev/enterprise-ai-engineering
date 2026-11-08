from fastapi.testclient import TestClient
from aiworkbench.main import app
from aiworkbench import repository

client = TestClient(app, headers={"X-API-Key": "ci-test-key"})


def use_database(tmp_path, monkeypatch):
    monkeypatch.setattr(repository, "database_path", lambda: str(tmp_path / "workbench.db"))


def good_patch():
    return {
        "src/app.py": "def health_check():\n    return {'status': 'ok'}\n",
        "tests/test_app.py": "def test_health_check():\n    assert True\n",
    }


def evaluate_patch(files):
    return client.post("/v1/evaluations", json={
        "task_id": "api-health-endpoint", "agent_profile": "synthetic-agent-v1",
        "patch_files": files
    })


def test_health_and_task_catalogue():
    assert client.get("/health").status_code == 200
    assert client.get("/v1/tasks").json()[0]["task_id"] == "api-health-endpoint"


def test_complete_patch_receives_full_static_score(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = evaluate_patch(good_patch())
    assert response.status_code == 201
    assert response.json()["score"] == 100
    assert response.json()["merge_eligible"] is True
    assert response.json()["test_execution"].startswith("NOT_RUN")


def test_missing_acceptance_file_reduces_score(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = evaluate_patch({"src/app.py": "def health_check(): pass"})
    assert response.json()["acceptance_score"] < 60
    assert response.json()["merge_eligible"] is False


def test_secret_pattern_blocks_merge_eligibility(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    patch = good_patch()
    patch["src/app.py"] += "\nAPI_KEY = 'synthetic-but-secret-looking-value'\n"
    response = evaluate_patch(patch)
    assert response.json()["security_score"] == 0
    assert response.json()["merge_eligible"] is False


def test_unsafe_execution_pattern_is_flagged(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    patch = good_patch()
    patch["src/app.py"] += "\nimport os\nos.system('echo unsafe')\n"
    response = evaluate_patch(patch)
    assert response.json()["security_findings"]


def test_unknown_task_returns_404(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    response = client.post("/v1/evaluations", json={
        "task_id": "unknown-task", "agent_profile": "synthetic-agent",
        "patch_files": good_patch()
    })
    assert response.status_code == 404


def test_report_is_persisted(tmp_path, monkeypatch):
    use_database(tmp_path, monkeypatch)
    created = evaluate_patch(good_patch()).json()
    fetched = client.get(f"/v1/evaluations/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["score"] == 100


def test_malformed_request_id_is_replaced():
    response = client.get("/health", headers={"X-Request-ID": "invalid request id"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] != "invalid request id"
    assert len(response.headers["x-request-id"]) == 32

def test_protected_api_rejects_missing_api_key():
    unauthenticated = TestClient(app)
    response = unauthenticated.get("/openapi.json")
    assert response.status_code == 401
    wrong_key = TestClient(app, headers={"X-API-Key": "incorrect-test-key"})
    assert wrong_key.get("/openapi.json").status_code == 401


def test_api_fails_closed_when_server_key_is_unconfigured(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    response = TestClient(app).get("/openapi.json")
    assert response.status_code == 503
