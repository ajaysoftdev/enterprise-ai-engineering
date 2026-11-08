"""Provider-neutral HTTP adapters for existing portfolio domain services."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class AdapterError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _request_json(url: str, method: str = "GET", payload: dict | None = None, timeout: float = 5.0, request_id: str | None = None, api_key: str | None = None):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise AdapterError("Downstream URL must use HTTP or HTTPS")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if request_id:
        headers["X-Request-ID"] = request_id
    if api_key:
        headers["X-API-Key"] = api_key
    request = Request(url, data=data, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec B310 - URL scheme is restricted above
            body = response.read()
            return json.loads(body) if body else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise AdapterError(f"Downstream HTTP {exc.code}: {detail}", exc.code) from exc
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"Downstream request failed: {type(exc).__name__}") from exc


class DocumentIntelligenceAdapter:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.getenv("DOCINT_URL", "http://localhost:8001")).rstrip("/")
        self.api_key = os.getenv("DOCINT_API_KEY")

    def submit(self, payload: dict, request_id: str | None = None) -> dict:
        return _request_json(f"{self.base_url}/v1/documents", "POST", payload, request_id=request_id, api_key=self.api_key)


class MdmAdapter:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.getenv("MDM_URL", "http://localhost:8002")).rstrip("/")
        self.api_key = os.getenv("MDM_API_KEY")

    def create_supplier(self, payload: dict, request_id: str | None = None) -> dict:
        return _request_json(f"{self.base_url}/v1/source-records", "POST", payload, request_id=request_id, api_key=self.api_key)

    def refresh(self, candidate_id: str, source_record_id: str, request_id: str | None = None) -> dict:
        candidates = _request_json(f"{self.base_url}/v1/match-candidates", request_id=request_id, api_key=self.api_key)
        candidate = next((item for item in candidates if item["id"] == candidate_id), None)
        if candidate is None:
            raise AdapterError("MDM match candidate was not found")
        if candidate["status"] == "PENDING":
            return {"candidate_status": "PENDING", "golden_record_id": None}
        golden_records = _request_json(f"{self.base_url}/v1/golden-records", request_id=request_id, api_key=self.api_key)
        golden = next(
            (item for item in golden_records if source_record_id in item["source_record_ids"]),
            None,
        )
        if golden is None:
            raise AdapterError("MDM decision is recorded but no golden record contains the source record")
        return {
            "candidate_status": candidate["status"],
            "golden_record_id": golden["id"],
        }
