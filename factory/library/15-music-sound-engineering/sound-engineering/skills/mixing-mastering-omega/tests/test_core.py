import unittest
from ..core import MixingMasteringOmega

class TestMixingMasteringOmega(unittest.TestCase):
    def setUp(self):
        self.audio = MixingMasteringOmega()

    def test_audit_low_end_physics_stable(self):
        # 50Hz and 80Hz - well separated
        result = self.audio.audit_low_end_physics(50.0, 80.0)
        self.assertTrue(result["is_standard"])
        self.assertEqual(result["separation_hz"], 30.0)

    def test_audit_low_end_physics_clash(self):
        # 50Hz and 55Hz - frequency masking
        result = self.audio.audit_low_end_physics(50.0, 55.0)
        self.assertFalse(result["is_standard"])

    def test_audit_loudness_targets_techno(self):
        # -7 LUFS is optimal for techno
        result = self.audio.audit_loudness_targets(-7.0, "techno")
        self.assertTrue(result["is_standard"])
        self.assertEqual(result["status"], "OPTIMAL")

    def test_audit_loudness_targets_ambient_thin(self):
        # -16 LUFS is too thin even for ambient
        result = self.audio.audit_loudness_targets(-16.0, "ambient")
        self.assertFalse(result["is_standard"])
        self.assertEqual(result["status"], "THIN")

    def test_verify_mono_compatibility_safe(self):
        result = self.audio.verify_mono_compatibility(0.8)
        self.assertTrue(result["is_mono_compatible"])
        self.assertEqual(result["risk"], "LOW")

    def test_verify_mono_compatibility_critical(self):
        result = self.audio.verify_mono_compatibility(-0.6)
        self.assertFalse(result["is_mono_compatible"])
        self.assertEqual(result["risk"], "CRITICAL")

if __name__ == '__main__':
    unittest.main()
