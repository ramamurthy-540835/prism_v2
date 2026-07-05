import os
from typing import Any

import requests

class PrismV1Client:
    def __init__(self, base_url: str | None = None, timeout: int = 120):
        self.base_url = (base_url or os.getenv("PRISM_V1_BASE_URL") or "").rstrip("/")
        self.timeout = timeout

    @property
    def mock(self) -> bool:
        return not self.base_url or os.getenv("PRISM_V1_MOCK", "").lower() in {"1", "true", "yes"}

    def send(self, payload: dict[str, Any], operation: str = "plan") -> dict[str, Any]:
        if self.mock:
            return {
                "bridge": "prism_v1",
                "mode": "mock",
                "operation": operation,
                "success": True,
                "received": payload,
            }
        endpoint = f"{self.base_url}/api/coder/{operation}"
        request_payload = {"task": payload, "mode": operation, "prompt_uid": payload.get("prompt_uid")}
        response = requests.post(
            endpoint,
            json=request_payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        response_payload = response.json()
        if isinstance(response_payload, dict):
            response_payload.setdefault("bridge", "prism_v1")
            response_payload.setdefault("mode", operation)
            response_payload["prism_v1_endpoint"] = endpoint
            response_payload["prism_v1_request"] = request_payload
        return response_payload
