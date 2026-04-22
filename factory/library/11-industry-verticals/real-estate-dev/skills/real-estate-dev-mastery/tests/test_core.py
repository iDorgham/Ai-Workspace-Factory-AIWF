import unittest
from ..core import RealEstateDevMastery

class TestRealEstateDevMastery(unittest.TestCase):
    def setUp(self):
        self.re = RealEstateDevMastery()

    def test_calculate_property_valuation(self):
        prop = {"area_sqft": 1000, "target_annual_rent": 100000}
        comps = {"prices": [1500, 1600, 1400], "avg_cap_rate": 0.07}
        # Comp value: 1500 * 1000 = 1,500,000
        # Income value: (100,000 * 0.85) / 0.07 = 1,214,285.71
        # Weighted: (1,500,000 * 0.6) + (1,214,285.71 * 0.4) = 900,000 + 485,714.28 = 1,385,714.28
        result = self.re.calculate_property_valuation(prop, comps)
        self.assertAlmostEqual(result["estimated_market_value"], 1385714.29, delta=1)

    def test_solve_irr(self):
        # Invest 100, get 110 in year 1
        cash_flows = [-100, 110]
        irr = self.re.solve_irr(cash_flows)
        self.assertEqual(irr, 0.1)

    def test_solve_irr_complex(self):
        # Traditional cash flows
        cash_flows = [-100, 30, 40, 50]
        irr = self.re.solve_irr(cash_flows)
        self.assertGreater(irr, 0.05)

    def test_audit_mena_transaction_costs_dubai(self):
        price = 1000000
        result = self.re.audit_mena_transaction_costs(price, "Dubai")
        self.assertEqual(result["cost_breakdown"]["dld_fee"], 40000)
        self.assertEqual(result["total_transaction_costs"], 64000) # 40k + 4k + 20k

    def test_audit_project_lifecycle(self):
        state = {
            "milestones": [
                {"status": "verified_complete", "is_delayed": False},
                {"status": "in_progress", "is_delayed": True}
            ]
        }
        result = self.re.audit_project_lifecycle(state)
        self.assertEqual(result["completion_percentage"], 50.0)
        self.assertEqual(result["risk_status"], "STABLE") # Only 1 delay is stable in this heuristic

    def test_calculate_regulatory_score_omega(self):
        data = {"escrow_account_verified": True, "rera_registered": True, "permit_valid": True}
        result = self.re.calculate_regulatory_score(data)
        self.assertEqual(result["regulatory_score"], 100)
        self.assertEqual(result["trust_tier"], "OMEGA")

if __name__ == '__main__':
    unittest.main()
