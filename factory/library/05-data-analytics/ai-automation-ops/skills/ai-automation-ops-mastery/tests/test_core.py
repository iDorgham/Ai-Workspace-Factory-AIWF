import unittest
from ..core import AiAutomationOpsMastery

class TestAiAutomationOpsMastery(unittest.TestCase):
    def setUp(self):
        self.aiops = AiAutomationOpsMastery()

    def test_audit_resource_costs_within_budget(self):
        pipeline = {"tokens_used": 100000, "cost_per_token": 0.00001, "infra_fixed_cost": 2.0}
        result = self.aiops.audit_resource_costs(pipeline, 5.0)
        self.assertTrue(result["is_within_budget"])
        self.assertEqual(result["total_actual_cost"], 3.0)

    def test_audit_resource_costs_over_budget(self):
        pipeline = {"tokens_used": 500000, "cost_per_token": 0.00001, "infra_fixed_cost": 1.0}
        result = self.aiops.audit_resource_costs(pipeline, 5.0)
        self.assertTrue(result["critical_warning"]) # 6.0 > 4.5
        self.assertFalse(result["is_within_budget"])

    def test_monitor_sla_compliance_pass(self):
        executions = [
            {"status": "success", "latency_ms": 200},
            {"status": "success", "latency_ms": 300}
        ]
        result = self.aiops.monitor_sla_compliance(executions)
        self.assertTrue(result["is_sla_compliant"])
        self.assertEqual(result["success_rate_percent"], 100.0)

    def test_detect_pipeline_bottlenecks(self):
        steps = [
            {"name": "Fetch Data", "duration_ms": 500},
            {"name": "Heavy LLM Task", "duration_ms": 5000}
        ]
        bottlenecks = self.aiops.detect_pipeline_bottlenecks(steps)
        self.assertEqual(len(bottlenecks), 1)
        self.assertIn("Heavy LLM Task", bottlenecks[0])

if __name__ == '__main__':
    unittest.main()
