import unittest
from ..core import WebDevelopingMastery

class TestWebDevelopingMastery(unittest.TestCase):
    def setUp(self):
        self.web = WebDevelopingMastery()

    def test_run_performance_audit_pass(self):
        metrics = {"LCP": 1200, "FID": 50, "CLS": 0.05}
        result = self.web.run_performance_audit(metrics)
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["meets_omega_standard"])

    def test_run_performance_audit_fail(self):
        metrics = {"LCP": 5000, "FID": 50, "CLS": 0.05}
        result = self.web.run_performance_audit(metrics)
        self.assertEqual(result["score"], 66.66666666666666)
        self.assertFalse(result["meets_omega_standard"])

    def test_validate_accessibility_violations(self):
        html = '<img src="test.png"><button></button><input type="text">'
        violations = self.web.validate_accessibility(html)
        self.assertEqual(len(violations), 3)
        self.assertIn("Missing alt attribute", violations[0])
        self.assertIn("Empty <button>", violations[1])
        self.assertIn("associated <label>", violations[2])

    def test_audit_logical_properties_violation(self):
        css = "div { margin-left: 10px; padding-right: 5px; }"
        violations = self.web.audit_logical_properties(css)
        self.assertEqual(len(violations), 2)
        self.assertIn("margin-left", violations[0])

if __name__ == '__main__':
    unittest.main()
