import os
from typing import Any

import requests

class LakehouseClient:
    def __init__(self, base_url: str | None = None, timeout: int = 60):
        self.base_url = (base_url or os.getenv("PRISM_LAKEHOUSE_BASE_URL") or "").rstrip("/")
        self.timeout = timeout

    def get_rules(self, intent: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            return {
                "governance": "strict",
                "source": "local",
                "prompt_version": "local",
                "estimation_required": True,
                "allow_execute": True,
                "requires_approval": intent.get("operation") in {"apply", "deploy"},
            }
        response = requests.post(f"{self.base_url}/rules", json={"intent": intent}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
