import unittest
from ..core import CinematicMotionOrchestration

class TestCinematicMotionOrchestration(unittest.TestCase):
    def setUp(self):
        self.cine = CinematicMotionOrchestration()

    def test_audit_parallax_depth_valid(self):
        config = {
            "layers": [
                {"plane": "front", "motion": "fast"},
                {"plane": "middle", "motion": "mid"},
                {"plane": "back", "motion": "slow"}
            ]
        }
        result = self.cine.audit_parallax_depth(config)
        self.assertTrue(result["is_parallax_compliant"])
        self.assertEqual(result["status"], "CINEMATIC")

    def test_audit_parallax_depth_flat(self):
        config = {"layers": [{"plane": "middle"}]}
        result = self.cine.audit_parallax_depth(config)
        self.assertFalse(result["is_parallax_compliant"])
        self.assertEqual(result["status"], "FLAT_MOTION")

    def test_validate_color_grade_luxury(self):
        metrics = {"sky_hue": "deep_azure", "shadow_temp": 4500, "highlight_temp": 6500}
        result = self.cine.validate_color_grade(metrics)
        self.assertTrue(result["is_luxury_grade"])
        self.assertEqual(result["tone_profile"], "GOLDEN_HOUR")

    def test_validate_color_grade_generic(self):
        metrics = {"sky_hue": "grey", "shadow_temp": 6500, "highlight_temp": 6500}
        result = self.cine.validate_color_grade(metrics)
        self.assertFalse(result["is_luxury_grade"])

    def test_score_temporal_consistency_high(self):
        seq = [{"has_wobble": False} for _ in range(100)]
        result = self.cine.score_temporal_consistency(seq)
        self.assertEqual(result["consistency_score"], 100.0)
        self.assertTrue(result["is_stabilized"])

    def test_score_temporal_consistency_low(self):
        seq = [{"has_wobble": True} for _ in range(10)] + [{"has_wobble": False} for _ in range(10)]
        result = self.cine.score_temporal_consistency(seq)
        self.assertEqual(result["consistency_score"], 50.0)
        self.assertFalse(result["is_stabilized"])

if __name__ == '__main__':
    unittest.main()
