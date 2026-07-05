from kernel.agents.base import Agent

class CoderAgent(Agent):
    name = "coder"

    def run(self, node: dict, model: str, **kwargs) -> dict:
        intent = kwargs.get("intent", {})
        return {
            "agent": self.name,
            "operation": node.get("operation", "apply"),
            "model": model,
            "task": intent.get("raw_task"),
            "prompt_uid": intent.get("prompt_uid"),
            "status": "ready_for_prism_v1",
        }
