import unittest
from ..core import DataSovereigntyMastery

class TestDataSovereigntyMastery(unittest.TestCase):
    def setUp(self):
        self.sovereignty = DataSovereigntyMastery()

    def test_audit_mana_localization_sovereign(self):
        arch = {"storage_node_regions": ["uae-north", "eu-west-1"]}
        result = self.sovereignty.audit_mana_localization(arch)
        self.assertTrue(result["pii_localized"])
        self.assertEqual(result["status"], "SOVEREIGN")

    def test_audit_mana_localization_non_compliant(self):
        arch = {"storage_node_regions": ["us-east-1"]}
        result = self.sovereignty.audit_mana_localization(arch)
        self.assertFalse(result["pii_localized"])
        self.assertEqual(result["status"], "NON_COMPLIANT_OFFSHORE")

    def test_calculate_sovereignty_risk_low(self):
        vectors = {"on_prem_or_local_cloud": True, "regional_kms_active": True, "cross_border_sharing_legal_active": True}
        result = self.sovereignty.calculate_sovereignty_risk(vectors)
        self.assertEqual(result["sovereignty_score"], 100)
        self.assertEqual(result["risk_status"], "LOW")

    def test_validate_regional_dpa_controls_hardened(self):
        controls = {"dpo_assigned": True, "consent_lifecycle_active": True, "deletion_protocol_enforced": True}
        result = self.sovereignty.validate_regional_dpa_controls(controls, "UAE")
        self.assertTrue(result["is_dpa_compliant"])
        self.assertEqual(result["status"], "HARDENED")

if __name__ == '__main__':
    unittest.main()
