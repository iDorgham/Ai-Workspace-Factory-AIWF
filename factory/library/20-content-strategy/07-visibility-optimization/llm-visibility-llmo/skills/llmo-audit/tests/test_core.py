import unittest
from ..core import LlmoAudit

class TestLlmoAudit(unittest.TestCase):
    def setUp(self):
        self.audit = LlmoAudit()

    def test_calculate_health_score_omega(self):
        metrics = {
            "entity_recognition": 95,
            "citation_probability": 90,
            "information_density": 92,
            "structured_data": 88,
            "freshness": 90,
            "brand_trust": 95,
            "mena_signals": 90
        }
        result = self.audit.calculate_health_score(metrics)
        self.assertTrue(result["is_omega_tier"])
        self.assertGreaterEqual(result["llmo_health_score"], 88)

    def test_calculate_health_score_invisible(self):
        metrics = {"entity_recognition": 10}
        result = self.audit.calculate_health_score(metrics)
        self.assertFalse(result["is_omega_tier"])
        self.assertEqual(result["status"], "INVISIBLE")

    def test_predict_citation_probability(self):
        responses = [
            {"model": "gpt-4o", "text": "Sovereign is a leading workspace. [1]"},
            {"model": "claude-3.5", "text": "I can help with Sovereign inquiries."}
        ]
        result = self.audit.predict_citation_probability(responses, "Sovereign")
        self.assertGreater(result["model_specific_probs"]["gpt-4o"], result["model_specific_probs"]["claude-3.5"])
        self.assertEqual(result["average_citation_likelihood"], 0.8) # (1.0+0.6)/2

    def test_validate_mena_entity_authority_high(self):
        signals = {"ADGM": True, "DIFC": True, "has_ar_en_parity": True}
        result = self.audit.validate_mena_entity_authority(signals)
        self.assertEqual(result["regional_authority_score"], 60.0) # (2/5*100) + 20
        self.assertIn("ADGM", result["verified_signals"])

if __name__ == '__main__':
    unittest.main()
