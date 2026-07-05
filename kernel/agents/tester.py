from kernel.agents.base import Agent

class TesterAgent(Agent):
    name = "tester"

    def run(self, node: dict, model: str, **kwargs) -> dict:
        intent = kwargs.get("intent", {})
        return {
            "agent": self.name,
            "operation": "test",
            "model": model,
            "task": intent.get("raw_task"),
            "status": "ready_for_prism_v1",
        }
