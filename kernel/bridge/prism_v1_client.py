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
        response = requests.post(
            f"{self.base_url}/api/coder/{operation}",
            json={"task": payload, "mode": operation, "prompt_uid": payload.get("prompt_uid")},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
