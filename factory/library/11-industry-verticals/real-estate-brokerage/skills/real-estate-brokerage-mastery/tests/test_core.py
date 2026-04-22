import unittest
from ..core import RealEstateBrokerageMastery

class TestRealEstateBrokerageMastery(unittest.TestCase):
    def setUp(self):
        self.re = RealEstateBrokerageMastery()

    def test_reconcile_inventory_parity(self):
        units = [{"unit_id": "UNIT_001", "price": 1000, "status": "AVAILABLE"}]
        ledger = [{"unit_id": "UNIT_001", "price": 1000, "status": "AVAILABLE"}]
        result = self.re.reconcile_inventory(units, ledger)
        self.assertEqual(result["reconciliation_score"], 1.0)
        self.assertEqual(result["status"], "OMEGA_PARITY")

    def test_enrich_luxury_lead_qualified(self):
        lead = {"id": "HNW_001", "investment_intent": "HIGH_FIDELITY"}
        kyc = {"kyc_tier": 3, "is_pep": False}
        result = self.re.enrich_luxury_lead(lead, kyc)
        self.assertEqual(result["qualification_status"], "OMEGA_QUALIFIED")
        self.assertEqual(result["recommended_action"], "PRIORITY_HNDOVER")

if __name__ == '__main__':
    unittest.main()
