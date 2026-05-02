import unittest
from ..core import QualityAssuranceMastery
import os
from unittest.mock import patch

class TestQualityAssuranceMastery(unittest.TestCase):
    def setUp(self):
        self.qa = QualityAssuranceMastery()

    @patch('os.path.exists')
    def test_audit_library_health_healthy(self, mock_exists):
        # Every check returns True
        mock_exists.return_value = True
        nodes = ["node1", "node2"]
        result = self.qa.audit_library_health(nodes)
        self.assertEqual(result["health_score"], 100.0)
        self.assertEqual(result["status"], "HEALTHY")

    @patch('os.path.exists')
    def test_audit_library_health_degraded(self, mock_exists):
        # Mock some missing files
        def side_effect(path):
            if "SKILL.md" in path: return False
            return True
        mock_exists.side_effect = side_effect
        
        nodes = ["node1"]
        result = self.qa.audit_library_health(nodes)
        self.assertEqual(result["health_score"], 0.0)
        self.assertEqual(result["violation_count"], 1)
        self.assertIn("SKILL.md", result["violations"][0]["missing"])

    def test_run_smoke_test_engine_pass(self):
        results = [{"node": "n1", "passed": True}, {"node": "n2", "passed": True}]
        result = self.qa.run_smoke_test_engine(results)
        self.assertTrue(result["is_smoke_pass"])
        self.assertEqual(result["recommendation"], "BASELINE_STABLE")

    def test_run_smoke_test_engine_fail(self):
        results = [{"node": "n1", "passed": False}]
        result = self.qa.run_smoke_test_engine(results)
        self.assertFalse(result["is_smoke_pass"])
        self.assertEqual(result["failed_nodes"], ["n1"])

if __name__ == '__main__':
    unittest.main()
