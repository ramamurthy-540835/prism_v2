class PolicyEngine:
    BLOCKED_TYPES = {"dangerous"}

    def validate(self, intent: dict, rules: dict) -> bool:
        if intent.get("type") in self.BLOCKED_TYPES:
            return False
        if rules.get("allow_execute") is False:
            return False
        return True

    def validate_or_raise(self, intent: dict, rules: dict) -> None:
        if not self.validate(intent, rules):
            raise PermissionError("PRISM v2 policy blocked execution")
