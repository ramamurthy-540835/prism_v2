import unittest

from kernel.core import PrismKernel
from kernel.bridge.prism_v1_client import PrismV1Client
from kernel.graph.builder import GraphBuilder
from kernel.intent.classifier import IntentClassifier
from kernel.intent.parser import IntentParser

class PrismKernelTests(unittest.TestCase):
    def test_run_local_mock_bridge(self):
        kernel = PrismKernel()
        result = kernel.run("build api service", operation="plan")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["results"][-1]["mode"], "mock")
        self.assertEqual(result["results"][-1]["operation"], "plan")

    def test_prompt_uid_parse(self):
        parsed = IntentParser().parse("fix vertexai:3381323161097207808")
        self.assertEqual(parsed["prompt_uid"], "vertexai:3381323161097207808")

    def test_deploy_graph_contains_test_gate(self):
        parsed = IntentParser().parse("deploy app", operation="deploy")
        intent = IntentClassifier().classify(parsed)
        graph = GraphBuilder().build(intent, {}, {})
        self.assertEqual([node.id for node in graph], ["plan", "code", "test", "deploy"])

    def test_bridge_mock_without_base_url(self):
        bridge = PrismV1Client(base_url="")
        result = bridge.send({"hello": "world"}, operation="plan")
        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "mock")

if __name__ == "__main__":
    unittest.main()
