import unittest
from ..core import LegalBrokerageMastery

class TestLegalBrokerageMastery(unittest.TestCase):
    def setUp(self):
        self.legal = LegalBrokerageMastery()

    def test_audit_contract_integrity_vc_pass(self):
        contract = {
            "valuation_cap": 5000000,
            "discount_rate": 0.8,
            "governing_law": "ADGM, Abu Dhabi",
            "liquidity_event_definition": "Defined",
            "pro_rata_rights": "Yes"
        }
        result = self.legal.audit_contract_integrity_vc(contract)
        self.assertTrue(result["is_integral"])
        self.assertEqual(result["law_compliance"], "VALID_JURISDICTION")
        self.assertEqual(result["tier"], "💎 OMEGA")

    def test_audit_contract_integrity_vc_fail(self):
        contract = {
            "valuation_cap": 5000000,
            "governing_law": "None" # Invalid jurisdiction
        }
        result = self.legal.audit_contract_integrity_vc(contract)
        self.assertFalse(result["is_integral"])
        self.assertIn("discount_rate", result["missing_mandatory_clauses"])

    def test_generate_saft_physics_summary(self):
        terms = {"valuation_cap": 10000000, "discount": 0.2, "tge_clause": True}
        result = self.legal.generate_saft_physics_summary(terms)
        self.assertEqual(result["instrument_type"], "SAFT")
        self.assertEqual(result["investor_discount"], "20.0%")
        self.assertTrue(result["token_generation_event_ready"])

if __name__ == '__main__':
    unittest.main()
