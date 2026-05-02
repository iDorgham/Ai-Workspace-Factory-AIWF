import unittest
from ..core import VideoProductionMastery

class TestVideoProductionMastery(unittest.TestCase):
    def setUp(self):
        self.video = VideoProductionMastery()

    def test_audit_cinematic_bitrate_pass(self):
        stats = {"resolution": "4K", "bitrate_mbps": 45.0}
        result = self.video.audit_cinematic_bitrate(stats)
        self.assertTrue(result["is_bitrate_compliant"])
        self.assertEqual(result["status"], "CINEMATIC_READY")

    def test_audit_cinematic_bitrate_fail(self):
        stats = {"resolution": "4K", "bitrate_mbps": 12.0}
        result = self.video.audit_cinematic_bitrate(stats)
        self.assertFalse(result["is_bitrate_compliant"])
        self.assertEqual(result["status"], "LOW_FIDELITY_BLOCK")

    def test_verify_color_space_guard_valid(self):
        meta = {"color_space": "Rec.709"}
        result = self.video.verify_color_space_guard(meta)
        self.assertTrue(result["is_brand_standard"])

    def test_calculate_storytelling_density_omega(self):
        meta = {"cut_timestamps": [0, 1.5, 4, 6]}
        result = self.video.calculate_storytelling_density(meta)
        self.assertTrue(result["is_scroll_stop_ready"])
        self.assertEqual(result["density_tier"], "OMEGA_HOOK")

if __name__ == '__main__':
    unittest.main()
