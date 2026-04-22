import unittest
from ..core import VideoScriptingMastery

class TestVideoScriptingMastery(unittest.TestCase):
    def setUp(self):
        self.scripting = VideoScriptingMastery()

    def test_audit_script_retention_short_pass(self):
        script = "Why the industry is lying to you in 2026. This is the secret. Follow for more."
        result = self.scripting.audit_script_retention(script, "short")
        self.assertTrue(result["has_scroll_stop_hook"])
        self.assertTrue(result["has_cta"])
        self.assertGreaterEqual(result["retention_score"], 70)

    def test_audit_script_retention_fail(self):
        script = "This is a dull video about architecture with no hook or call to action."
        result = self.scripting.audit_script_retention(script, "short")
        self.assertFalse(result["has_scroll_stop_hook"])
        self.assertFalse(result["has_cta"])
        self.assertLess(result["retention_score"], 50)

    def test_validate_regional_flow_masri(self):
        script = "يا تمام، let's discuss UI design for the Cairo market."
        result = self.scripting.validate_regional_flow(script, "Masri")
        self.assertIn("يا", result["regional_cues"])
        self.assertIn("ui", result["tech_terms"])
        self.assertEqual(result["linguistic_flow_score"], 1.0)

    def test_calculate_pacing_metrics(self):
        # 75 words should take ~30 seconds at 150 WPM
        script = "word " * 75
        result = self.scripting.calculate_pacing_metrics(script, 30)
        self.assertEqual(result["predicted_duration_sec"], 30.0)
        self.assertEqual(result["status"], "on_target")

    def test_generate_hbco_script(self):
        data = {"hook": "Stop!", "bridge": "Look.", "content": "Learn.", "offer": "Buy."}
        result = self.scripting.generate_hbco_script(data)
        self.assertIn("HOOK: Stop!", result["script_text"])
        self.assertEqual(result["status"], "STRUCTURE_READY")

if __name__ == '__main__':
    unittest.main()
