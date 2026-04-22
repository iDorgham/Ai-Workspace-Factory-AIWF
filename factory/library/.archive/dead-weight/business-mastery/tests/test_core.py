import unittest
from ..core import BusinessMastery

class TestBusinessMastery(unittest.TestCase):
    def setUp(self):
        self.business = BusinessMastery()

    def test_audit_unit_economics_healthy(self):
        data = {"cac": 100, "ltv": 400, "mrr_per_customer": 50}
        result = self.business.audit_unit_economics(data)
        self.assertEqual(result["status"], "HEALTHY")
        self.assertTrue(result["meets_omega_benchmark"])
        self.assertEqual(result["payback_months"], 2.0)

    def test_audit_unit_economics_inefficient(self):
        data = {"cac": 1000, "ltv": 2000, "mrr_per_customer": 50}
        result = self.business.audit_unit_economics(data)
        self.assertEqual(result["status"], "INEFFICIENT") # Payback > 12 months

    def test_validate_regional_incorporation(self):
        checklist = ["commercial_license", "office_lease"]
        result = self.business.validate_regional_incorporation("ADGM", checklist)
        self.assertFalse(result["is_complete"])
        self.assertIn("data_protection_filing", result["missing_steps"])

    def test_project_scaling_runway(self):
        self.assertEqual(self.business.project_scaling_runway(100000, 10000), 10)
        self.assertEqual(self.business.project_scaling_runway(100000, 0), 999)

if __name__ == '__main__':
    unittest.main()
