from kernel.agents.base import Agent

class PlannerAgent(Agent):
    name = "planner"

    def run(self, node: dict, model: str, **kwargs) -> dict:
        intent = kwargs.get("intent", {})
        return {
            "agent": self.name,
            "type": "plan",
            "model": model,
            "plan": ["parse_intent", "load_governance", "build_dag", "delegate_to_prism_v1"],
            "intent_type": intent.get("type"),
        }
