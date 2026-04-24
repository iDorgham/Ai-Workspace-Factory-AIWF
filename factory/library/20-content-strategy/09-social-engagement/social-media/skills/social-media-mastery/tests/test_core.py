import unittest
from ..core import SocialMediaMastery

class TestSocialMediaMastery(unittest.TestCase):
    def setUp(self):
        self.social = SocialMediaMastery()

    def test_audit_platform_tone_ig_pass(self):
        meta = {"platform": "Instagram", "tags": ["lifestyle", "luxury"], "has_high_res_visual": True}
        result = self.social.audit_platform_tone(meta)
        self.assertTrue(result["is_tone_compliant"])
        self.assertEqual(result["status"], "APPROVED")

    def test_validate_storytelling_fidelity_omega(self):
        config = {"resolution": 2160, "human_lifestyle_presence": True}
        result = self.social.validate_storytelling_fidelity(config)
        self.assertTrue(result["is_high_fidelity"])
        self.assertEqual(result["storytelling_grade"], "OMEGA")

    def test_calculate_virality_score_high(self):
        stats = {"views_first_10_min": 7000, "avg_watch_time_pct": 90.0, "shares": 100, "likes": 500}
        result = self.social.calculate_virality_score(stats)
        self.assertGreater(result["virality_score"], 80)
        self.assertTrue(result["is_trending_potential"])

if __name__ == '__main__':
    unittest.main()
