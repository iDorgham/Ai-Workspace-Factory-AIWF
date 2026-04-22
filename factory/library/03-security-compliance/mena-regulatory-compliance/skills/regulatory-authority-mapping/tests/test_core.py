import unittest
from ..core import RegulatoryAuthorityMapping

class TestRegulatoryAuthorityMapping(unittest.TestCase):
    def setUp(self):
        self.reg = RegulatoryAuthorityMapping()

    def test_route_to_regulator_dubai_crypto(self):
        model = {"region": "Mainland Dubai", "activity": "Crypto Exchange"}
        result = self.reg.route_to_regulator(model)
        self.assertEqual(result["authority"], "VARA")
        self.assertEqual(result["jurisdiction"], "Dubai (Non-DIFC)")

    def test_route_to_regulator_difc_banking(self):
        model = {"region": "DIFC Dubai", "activity": "Banking Services"}
        result = self.reg.route_to_regulator(model)
        self.assertEqual(result["authority"], "DFSA")

    def test_route_to_regulator_egypt_payments(self):
        model = {"region": "Egypt", "activity": "Digital Payment Wallet"}
        result = self.reg.route_to_regulator(model)
        self.assertEqual(result["authority"], "CBE")

    def test_audit_data_sovereignty_fail(self):
        arch = {"data_type": "Financial Records", "storage_region": "AWS US-East", "company_region": "UAE"}
        result = self.reg.audit_data_sovereignty(arch)
        self.assertEqual(result["status"], "DATA_SOVEREIGNTY_RISK")
        self.assertTrue(result["needs_localization"])

    def test_audit_data_sovereignty_pass(self):
        arch = {"data_type": "Marketing Data", "storage_region": "Global"}
        result = self.reg.audit_data_sovereignty(arch)
        self.assertEqual(result["status"], "COMPLIANT")

    def test_validate_anti_patterns_invalid(self):
        path = {"selected_authority": "DED", "activity": "Web3 Platform"}
        result = self.reg.validate_anti_patterns(path)
        self.assertFalse(result["is_path_valid"])
        self.assertIn("VARA", result["blocker_reason"])

if __name__ == '__main__':
    unittest.main()
