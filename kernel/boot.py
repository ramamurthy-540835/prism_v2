from kernel.agents.coder import CoderAgent
from kernel.agents.planner import PlannerAgent
from kernel.agents.tester import TesterAgent
from kernel.bridge.prism_v1_client import PrismV1Client
from kernel.graph.builder import GraphBuilder
from kernel.graph.scheduler import GraphScheduler
from kernel.intent.classifier import IntentClassifier
from kernel.intent.parser import IntentParser
from kernel.lakehouse.client import LakehouseClient
from kernel.memory.state import State
from kernel.routing.router import ModelRouter
from kernel.safety.policy import PolicyEngine
from kernel.types import KernelRequest, KernelResult

class BootLoader:
    def __init__(self):
        self.intent_parser = IntentParser()
        self.intent_classifier = IntentClassifier()
        self.graph_builder = GraphBuilder()
        self.scheduler = GraphScheduler()
        self.router = ModelRouter()
        self.lakehouse = LakehouseClient()
        self.bridge = PrismV1Client()
        self.policy = PolicyEngine()
        self.state = State()
        self.agents = {
            "planner": PlannerAgent(),
            "coder": CoderAgent(),
            "tester": TesterAgent(),
        }
        self.initialized = False

    def initialize(self):
        self.initialized = True

    def execute(self, request: KernelRequest) -> KernelResult:
        parsed = self.intent_parser.parse(request.task, operation=request.operation)
        intent = self.intent_classifier.classify(parsed)
        rules = self.lakehouse.get_rules(intent)
        self.policy.validate_or_raise(intent, rules)
        graph = self.graph_builder.build(intent, rules, request.context)
        results = []

        for node in self.scheduler.ordered(graph):
            model = self.router.select(node.to_dict(), intent, rules)
            agent = self.agents[node.agent]
            output = agent.run(node.to_dict(), model, intent=intent, rules=rules, context=request.context)
            if node.type == "execute":
                output = self.bridge.send(output, operation=node.operation)
            results.append(output)
            if isinstance(output, dict) and output.get("error"):
                break

        status = "success" if all(not r.get("error") for r in results) else "error"
        result = KernelResult(
            request_id=request.request_id,
            status=status,
            intent=intent,
            graph=[node.to_dict() for node in graph],
            results=results,
        )
        self.state.save(request.request_id, result.to_dict())
        return result
