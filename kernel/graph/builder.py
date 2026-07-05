from kernel.types import GraphNode

class GraphBuilder:
    def build(self, intent: dict, rules: dict, context: dict | None = None) -> list[GraphNode]:
        operation = intent.get("operation") or "plan"
        graph = [
            GraphNode(id="plan", agent="planner", type="plan", operation="plan", payload={"context": context or {}}),
        ]
        if operation in {"apply", "test", "deploy"}:
            graph.append(GraphNode(id="code", agent="coder", type="execute", operation="apply", depends_on=["plan"]))
        if operation in {"test", "deploy"}:
            graph.append(GraphNode(id="test", agent="tester", type="execute", operation="test", depends_on=["code"]))
        if operation == "deploy":
            graph.append(GraphNode(id="deploy", agent="coder", type="execute", operation="deploy", depends_on=["test"]))
        if operation == "plan":
            graph.append(GraphNode(id="route", agent="coder", type="execute", operation="plan", depends_on=["plan"]))
        return graph
