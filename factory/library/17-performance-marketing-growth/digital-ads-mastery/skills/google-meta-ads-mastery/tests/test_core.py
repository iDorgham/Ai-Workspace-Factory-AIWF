import unittest
from ..core import GoogleMetaAdsMastery

class TestGoogleMetaAdsMastery(unittest.TestCase):
    def setUp(self):
        self.ads = GoogleMetaAdsMastery()

    def test_audit_roas_scaling_stable(self):
        perf = {"roas": 4.5, "daily_budget": 100, "hours_since_change": 50}
        result = self.ads.audit_roas_scaling(perf)
        self.assertEqual(result["recommendation"], "SCALE_UP")
        self.assertEqual(result["new_recommended_budget"], 120.0)

    def test_audit_roas_scaling_too_soon(self):
        perf = {"roas": 4.5, "daily_budget": 100, "hours_since_change": 10}
        result = self.ads.audit_roas_scaling(perf)
        self.assertEqual(result["recommendation"], "WAIT_FOR_STABILITY")

    def test_verify_tracking_health_red(self):
        data = {"pixel_status": "active", "capi_status": "inactive"}
        result = self.ads.verify_tracking_health(data)
        self.assertFalse(result["is_tracking_healthy"])
        self.assertEqual(result["status"], "RED")

    def test_calculate_creative_refresh_urgency_high(self):
        data = {"days_active": 20, "ctr_trend": -0.2}
        result = self.ads.calculate_creative_refresh_urgency(data)
        self.assertEqual(result["refresh_urgency"], "HIGH")

if __name__ == '__main__':
    unittest.main()
