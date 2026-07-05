import re

class IntentParser:
    def parse(self, task: str, operation: str = "plan") -> dict:
        text = task.strip()
        prompt_match = re.search(r"(vertexai:\d+|\b\d{12,}\b)", text)
        prompt_uid = None
        if prompt_match:
            value = prompt_match.group(1)
            prompt_uid = value if value.startswith("vertexai:") else f"vertexai:{value}"
        return {
            "task": text,
            "operation": operation or self._operation(text),
            "prompt_uid": prompt_uid,
            "tokens": text.lower().split(),
        }

    def _operation(self, text: str) -> str:
        lowered = text.lower()
        if "deploy" in lowered:
            return "deploy"
        if "test" in lowered or "validate" in lowered:
            return "test"
        if "apply" in lowered or "fix" in lowered or "implement" in lowered:
            return "apply"
        return "plan"
