import unittest
from ..core import RealEstateModeling

class TestRealEstateModeling(unittest.TestCase):
    def setUp(self):
        self.re = RealEstateModeling()

    def test_calculate_valuation_benchmark(self):
        data = {
            "comparable_value": 1000000,
            "income_capitalized_value": 900000,
            "replacement_cost_value": 1100000,
            "currency": "AED"
        }
        result = self.re.calculate_valuation_benchmark(data)
        # (1M * 0.5) + (0.9M * 0.35) + (1.1M * 0.15) = 500k + 315k + 165k = 980k
        self.assertEqual(result["estimated_market_value"], 980000.0)
        self.assertEqual(result["confidence_score"], 0.95)

    def test_audit_pbr_mesh_budget_pass(self):
        meta = {"polygon_count": 30000, "file_size_mb": 0.8}
        result = self.re.audit_pbr_mesh_budget(meta)
        self.assertTrue(result["is_web_compliant"])
        self.assertEqual(result["status"], "APPROVED")

    def test_audit_pbr_mesh_budget_fail(self):
        meta = {"polygon_count": 200000, "file_size_mb": 5.0}
        result = self.re.audit_pbr_mesh_budget(meta)
        self.assertFalse(result["is_web_compliant"])
        self.assertEqual(result["vitals_impact"], "CRITICAL_LCP_RISK")

    def test_calculate_mena_transaction_costs_uae(self):
        result = self.re.calculate_mena_transaction_costs(1000000, "UAE")
        # 4% DLD + 2% Agency = 60k
        self.assertEqual(result["transaction_tax_fee"], 60000.0)

    def test_calculate_mena_transaction_costs_egypt(self):
        result = self.re.calculate_mena_transaction_costs(1000000, "EGYPT")
        # 2.5% RETT = 25k + 2k admin = 27k
        self.assertEqual(result["transaction_tax_fee"], 27000.0)

if __name__ == '__main__':
    unittest.main()
