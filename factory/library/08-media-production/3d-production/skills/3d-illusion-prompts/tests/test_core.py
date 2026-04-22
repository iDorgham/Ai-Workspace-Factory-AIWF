import unittest
from ..core import ThreeDIllusionPrompts

class TestThreeDIllusionPrompts(unittest.TestCase):
    def setUp(self):
        self.three_d = ThreeDIllusionPrompts()

    def test_audit_parallax_physics_fail_scale(self):
        layers = [
            {"translate_z": -2, "scale": 1.0} # Missing scale compensation
        ]
        result = self.three_d.audit_parallax_physics(layers)
        self.assertFalse(result["is_physically_consistent"])
        self.assertIn("requires scale > 1.0", result["violations"][0])

    def test_audit_parallax_physics_pass(self):
        layers = [
            {"translate_z": -2, "scale": 1.5},
            {"translate_z": 0, "scale": 1.0}
        ]
        result = self.three_d.audit_parallax_physics(layers)
        self.assertTrue(result["is_physically_consistent"])

    def test_validate_ai_prompt_premium(self):
        prompt = "Underwater photography, Red Sea coral reef, depth of field bokeh, cinematic lighting, 8K"
        result = self.three_d.validate_ai_prompt(prompt)
        self.assertTrue(result["is_premium_tier"])
        self.assertTrue(result["has_regional_context"])

    def test_validate_ai_prompt_weak(self):
        prompt = "a blue car"
        result = self.three_d.validate_ai_prompt(prompt)
        self.assertFalse(result["is_premium_tier"])

    def test_recommend_accessibility_fallbacks(self):
        fallbacks = self.three_d.recommend_accessibility_fallbacks(True)
        self.assertEqual(len(fallbacks), 2)
        self.assertIn("prefers-reduced-motion", fallbacks[0])

if __name__ == '__main__':
    unittest.main()
