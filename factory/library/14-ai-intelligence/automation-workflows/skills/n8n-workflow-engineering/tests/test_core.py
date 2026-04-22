import unittest
from ..core import N8NWorkflowEngineering

class TestN8NWorkflowEngineering(unittest.TestCase):
    def setUp(self):
        self.n8n = N8NWorkflowEngineering()

    def test_audit_error_compliance_fail(self):
        nodes = [
            {"name": "Trigger", "on_error": True},
            {"name": "HTTP Request", "on_error": False}
        ]
        result = self.n8n.audit_error_compliance(nodes)
        self.assertFalse(result["is_standard"])
        self.assertEqual(len(result["violations"]), 1)

    def test_audit_error_compliance_pass(self):
        nodes = [{"name": "Node1", "retry_on_fail": True}]
        result = self.n8n.audit_error_compliance(nodes)
        self.assertTrue(result["is_standard"])

    def test_implement_ai_router(self):
        dataset = [
            {"input": "fix this bug"},
            {"input": "how to pay my invoice"},
            {"input": "start onboarding"}
        ]
        result = self.n8n.implement_ai_router(dataset)
        self.assertEqual(result["cluster_breakdown"]["technical"], 1)
        self.assertEqual(result["cluster_breakdown"]["billing"], 1)
        self.assertEqual(result["cluster_breakdown"]["onboarding"], 1)

    def test_optimize_resource_usage_found(self):
        nodes = [
            {"name": "Node1", "type": "edit-binary"},
            {"name": "Node2", "type": "edit-binary"},
            {"name": "Node3", "strips_data": False}
        ]
        result = self.n8n.optimize_resource_usage(nodes)
        self.assertEqual(len(result["strategies_identified"]), 2)

if __name__ == '__main__':
    unittest.main()
