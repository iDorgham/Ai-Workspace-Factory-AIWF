import unittest
from ..core import IslamicFinanceMastery

class TestIslamicFinanceMastery(unittest.TestCase):
    def setUp(self):
        self.finance = IslamicFinanceMastery()

    def test_filter_sharia_compliance_pass(self):
        portfolio = [
            {"id": "A", "total_debt": 100, "market_cap": 1000, "forbidden_revenue_perc": 0.01}, # Debt 10%
        ]
        result = self.finance.filter_sharia_compliance(portfolio)
        self.assertIn("A", result["compliant_assets"])
        self.assertEqual(len(result["violations_detected"]), 0)

    def test_filter_sharia_compliance_fail(self):
        portfolio = [
            {"id": "B", "total_debt": 500, "market_cap": 1000, "forbidden_revenue_perc": 0.01}, # Debt 50% (Fail)
            {"id": "C", "total_debt": 100, "market_cap": 1000, "forbidden_revenue_perc": 0.10}, # Revenue 10% (Fail)
        ]
        result = self.finance.filter_sharia_compliance(portfolio)
        self.assertEqual(len(result["compliant_assets"]), 0)
        self.assertEqual(len(result["violations_detected"]), 2)

    def test_calculate_zakat(self):
        assets = {"cash": 10000, "inventory": 40000}
        result = self.finance.calculate_zakat(assets)
        # 50,000 * 2.5% = 1250
        self.assertEqual(result["zakat_due_amount"], 1250.0)

if __name__ == '__main__':
    unittest.main()
