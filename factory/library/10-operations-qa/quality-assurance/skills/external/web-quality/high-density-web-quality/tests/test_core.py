import unittest
from ..core import HighDensityWebQuality

class TestHighDensityWebQuality(unittest.TestCase):
    def setUp(self):
        self.qa = HighDensityWebQuality()

    def test_audit_performance_budget_pass(self):
        stats = {"initial_js_kb": 150.0}
        result = self.qa.audit_performance_budget(stats)
        self.assertTrue(result["is_compliant"])
        self.assertEqual(result["status"], "GREEN")

    def test_audit_performance_budget_fail(self):
        stats = {"initial_js_kb": 250.0}
        result = self.qa.audit_performance_budget(stats)
        self.assertFalse(result["is_compliant"])
        self.assertEqual(result["status"], "RED")

    def test_audit_visual_regression_pass(self):
        # 0.0005 < 0.001
        result = self.qa.audit_visual_regression(0.0005, dynamic_masking=False)
        self.assertTrue(result["is_within_threshold"])

    def test_audit_visual_regression_masking(self):
        # 0.0015 > 0.001 (raw), but with masking 0.00075 < 0.001
        result = self.qa.audit_visual_regression(0.0015, dynamic_masking=True)
        self.assertTrue(result["is_within_threshold"])

    def test_verify_asset_metadata_complete(self):
        meta = {
            "favicon": True, "og_image": True, "og_title": True, 
            "manifest_json": True, "twitter_card": True
        }
        result = self.qa.verify_asset_metadata(meta)
        self.assertTrue(result["all_assets_present"])
        self.assertEqual(result["compliance_score"], 100.0)

    def test_verify_asset_metadata_incomplete(self):
        meta = {"favicon": True}
        result = self.qa.verify_asset_metadata(meta)
        self.assertFalse(result["all_assets_present"])
        self.assertIn("og_image", result["missing_assets"])

    def test_calculate_accessibility_score_pass(self):
        axe_run = {"violations": [{"impact": "serious", "help": "Images must have alt text"}]}
        result = self.qa.calculate_accessibility_score(axe_run)
        self.assertEqual(result["a11y_score"], 95)
        self.assertTrue(result["is_omega_compliant"])
        self.assertEqual(result["status"], "PASS")

    def test_verify_compression_standards_fail(self):
        assets = [
            {"name": "app.js", "ext": ".js", "compressed": False},
            {"name": "style.css", "ext": ".css", "compressed": True, "saved_kb": 50}
        ]
        result = self.qa.verify_compression_standards(assets)
        self.assertFalse(result["compression_compliance"])
        self.assertEqual(result["non_compliant_assets"], ["app.js"])

if __name__ == '__main__':
    unittest.main()
