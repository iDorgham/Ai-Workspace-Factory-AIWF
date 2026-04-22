import unittest
from ..core import ProactiveAgentMastery

class TestProactiveAgentMastery(unittest.TestCase):
    def setUp(self):
        self.agent = ProactiveAgentMastery()

    def test_discover_environment_gaps_found(self):
        env = {"node": True, "npm": False} # npm missing
        result = self.agent.discover_environment_gaps("Install React app", env)
        self.assertTrue(result["has_gaps"])
        self.assertIn("npm", result["missing_dependencies"])

    def test_discover_environment_gaps_none(self):
        env = {"node": True, "npm": True}
        result = self.agent.discover_environment_gaps("Install React app", env)
        self.assertFalse(result["has_gaps"])

    def test_generate_state_summary_periodic(self):
        # 10 turns should trigger summary
        result = self.agent.generate_state_summary(10, 50.0)
        self.assertTrue(result["should_summarize"])
        self.assertEqual(result["trigger"], "PERIODIC_CHECK")

    def test_generate_state_summary_saturation(self):
        # 85% saturation should trigger summary even if turn 1
        result = self.agent.generate_state_summary(1, 85.0)
        self.assertTrue(result["should_summarize"])
        self.assertEqual(result["trigger"], "SATURATION_LIMIT")

    def test_calculate_risk_score_dangerous(self):
        action = {"type": "delete", "lines_impacted": 50, "dependency_depth": 3}
        result = self.agent.calculate_risk_score(action)
        self.assertFalse(result["is_autonomous_safe"])
        self.assertTrue(result["requires_approval"])
        # 50 (delete) + 10 (50 lines) + 15 (3 depth) = 75
        self.assertEqual(result["risk_score"], 75)

    def test_calculate_risk_score_safe(self):
        action = {"type": "write", "lines_impacted": 5, "dependency_depth": 0}
        result = self.agent.calculate_risk_score(action)
        self.assertTrue(result["is_autonomous_safe"])
        # 20 (write) + 1 (5 lines) + 0 (depth) = 21
        self.assertLess(result["risk_score"], 30)

if __name__ == '__main__':
    unittest.main()
