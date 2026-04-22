import unittest
from ..core import ViralEngagementEngineering

class TestViralEngagementEngineering(unittest.TestCase):
    def setUp(self):
        self.eng = ViralEngagementEngineering()

    def test_audit_exclusivity_loops_luxury(self):
        config = {"keys_per_user": 2, "requires_asset_verification": True}
        result = self.eng.audit_exclusivity_loops(config)
        self.assertTrue(result["is_luxury_compliant"])
        self.assertEqual(result["scarcity_factor"], "HIGH")

    def test_audit_exclusivity_loops_diluted(self):
        config = {"keys_per_user": 10, "requires_asset_verification": False}
        result = self.eng.audit_exclusivity_loops(config)
        self.assertFalse(result["is_luxury_compliant"])
        self.assertEqual(result["scarcity_factor"], "DILUTED")

    def test_calculate_vcp_score_elite(self):
        metrics = {"text_overlay_percentage": 5.0, "resolution_k": 4, "is_cinematic_motion": True}
        result = self.eng.calculate_vcp_score(metrics)
        self.assertEqual(result["vcp_score"], 100)
        self.assertTrue(result["is_brand_safe"])

    def test_calculate_vcp_score_low(self):
        metrics = {"text_overlay_percentage": 50.0, "resolution_k": 1}
        result = self.eng.calculate_vcp_score(metrics)
        self.assertLess(result["vcp_score"], 40)
        self.assertEqual(result["status"], "GENERIC")

    def test_audit_influence_shadowing_active(self):
        data = {"whale_wallet_monitors": True, "shadow_targets_per_conversion": 5}
        result = self.eng.audit_influence_shadowing(data)
        self.assertTrue(result["is_shadowing_active"])

if __name__ == '__main__':
    unittest.main()
