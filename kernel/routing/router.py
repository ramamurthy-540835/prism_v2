import json
import os
from pathlib import Path

DEFAULT_ROUTES = {
    "planner": "gemini-3.5-flash",
    "coder": "gpt-5-codex",
    "tester": "gemini-3.5-flash",
}

class ModelRouter:
    def __init__(self, config_path: str | None = None):
        self.config_path = Path(config_path or os.getenv("PRISM_MODEL_CONFIG", "")) if (config_path or os.getenv("PRISM_MODEL_CONFIG")) else None
        self.routes = self._load_routes()

    def select(self, node: dict, intent: dict | None = None, rules: dict | None = None) -> str:
        return self.routes.get(node.get("agent"), self.routes.get("default", "gemini-3.5-flash"))

    def _load_routes(self) -> dict:
        if not self.config_path or not self.config_path.exists():
            return DEFAULT_ROUTES.copy()
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        return {**DEFAULT_ROUTES, **data.get("routes", {})}
