from kernel.agents.base import Agent

class CoderAgent(Agent):
    name = "coder"

    def run(self, node: dict, model: str, **kwargs) -> dict:
        intent = kwargs.get("intent", {})
        context = kwargs.get("context", {}) or {}
        return {
            "agent": self.name,
            "operation": node.get("operation", "apply"),
            "model": model,
            "task": intent.get("raw_task"),
            "prompt_uid": intent.get("prompt_uid") or context.get("prompt_uid"),
            "version": context.get("version"),
            "workspace_id": context.get("workspace_id"),
            "project_name": context.get("project_name"),
            "approval": bool(context.get("approval") or context.get("approval_required")),
            "approval_required": bool(context.get("approval_required") or context.get("approval")),
            "status": "ready_for_prism_v1",
        }
