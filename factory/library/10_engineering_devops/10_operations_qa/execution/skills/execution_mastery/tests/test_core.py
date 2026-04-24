import unittest
from ..core import ExecutionMastery

class TestExecutionMastery(unittest.TestCase):
    def setUp(self):
        self.execution = ExecutionMastery()

    def test_verify_spec_parity_pass(self):
        spec = "- Add login button\n- Fix sidebar logo"
        code = "function addLoginButton() {}\n// fix sidebar logo mentioned here"
        result = self.execution.verify_spec_parity(spec, code)
        self.assertTrue(result["is_standard"])
        self.assertEqual(result["coverage_percentage"], 100)

    def test_verify_spec_parity_fail(self):
        spec = "- Feature Alpha\n- Feature Beta"
        code = "function alpha() {}"
        result = self.execution.verify_spec_parity(spec, code)
        self.assertFalse(result["is_standard"])
        self.assertIn("Feature Beta", result["missing_features"])

    def test_distill_anti_patterns(self):
        logs = [
            "2026-04-20 10:00:00 ERROR: File not found",
            "Success: build complete",
            "2026-04-20 10:05:00 Failure: Timeout"
        ]
        patterns = self.execution.distill_anti_patterns(logs)
        self.assertEqual(len(patterns), 2)
        self.assertIn("ERROR: File not found", patterns[0])
        self.assertIn("Failure: Timeout", patterns[1])

    def test_enforce_sdd_workflow(self):
        valid_state = "Starting planning phase, then execution, then verification."
        self.assertTrue(self.execution.enforce_sdd_workflow(valid_state))
        
        invalid_state = "Just executing the code directly."
        self.assertFalse(self.execution.enforce_sdd_workflow(invalid_state))

if __name__ == '__main__':
    unittest.main()
