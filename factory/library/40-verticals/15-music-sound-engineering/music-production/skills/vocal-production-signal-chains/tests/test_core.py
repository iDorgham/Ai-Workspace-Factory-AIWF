import unittest
from ..core import VocalProductionSignalChains

class TestVocalProductionSignalChains(unittest.TestCase):
    def setUp(self):
        self.vocal = VocalProductionSignalChains()

    def test_audit_signal_chain_linear(self):
        chain = ["Pitch", "Clean", "Tone", "Dynamics"]
        result = self.vocal.audit_signal_chain(chain)
        self.assertTrue(result["is_standard_chain"])

    def test_audit_signal_chain_nonlinear(self):
        chain = ["Dynamics", "Pitch"] # Compression before pitch is bad
        result = self.vocal.audit_signal_chain(chain)
        self.assertFalse(result["is_standard_chain"])
        self.assertIn("NON-LINEAR CHAIN", result["violations"][0])

    def test_calculate_de_esser_threshold(self):
        result = self.vocal.calculate_de_esser_threshold(-10.0, 4.0)
        self.assertEqual(result["recommended_threshold"], -14.0)

    def test_audit_dynamic_stages_transparent(self):
        stages = [3.0, 3.5]
        result = self.vocal.audit_dynamic_stages(stages)
        self.assertTrue(result["is_transparent"])

    def test_audit_dynamic_stages_aggressive(self):
        stages = [8.0]
        result = self.vocal.audit_dynamic_stages(stages)
        self.assertFalse(result["is_transparent"])
        self.assertIn("Excessive reduction", result["warnings"][0])

    def test_audit_spatial_integrity_clean(self):
        config = {"reverb_low_cut_hz": 550, "phase_aligned": True}
        result = self.vocal.audit_spatial_integrity(config)
        self.assertTrue(result["is_spatial_clean"])
        self.assertEqual(result["phase_status"], "ALIGNED")

    def test_audit_spatial_integrity_muddy(self):
        config = {"reverb_low_cut_hz": 100, "phase_aligned": False}
        result = self.vocal.audit_spatial_integrity(config)
        self.assertFalse(result["is_spatial_clean"])
        self.assertEqual(result["phase_status"], "PHASE_ISSUE")

if __name__ == '__main__':
    unittest.main()
