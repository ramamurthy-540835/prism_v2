class IntentClassifier:
    def classify(self, parsed: dict) -> dict:
        task = parsed["task"].lower()
        operation = parsed.get("operation", "plan")
        if any(word in task for word in ("fix", "bug", "error", "broken")):
            intent_type = "code_fix"
            priority = "high"
        elif any(word in task for word in ("build", "create", "implement", "api", "service")):
            intent_type = "build"
            priority = "medium"
        elif any(word in task for word in ("test", "validate")):
            intent_type = "test"
            priority = "medium"
        else:
            intent_type = "general"
            priority = "low"
        return {
            "type": intent_type,
            "priority": priority,
            "operation": operation,
            "raw_task": parsed["task"],
            "prompt_uid": parsed.get("prompt_uid"),
        }
