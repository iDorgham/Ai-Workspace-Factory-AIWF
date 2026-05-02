import unittest
from ..core import CopywritingMastery

class TestCopywritingMastery(unittest.TestCase):
    def setUp(self):
        self.copy = CopywritingMastery()

    def test_audit_aida_framework_pass(self):
        text = "STOP! Discover the most exclusive oasis in New Cairo. Finally live your luxury dream. Book now for high ROI."
        result = self.copy.audit_aida_framework(text)
        self.assertEqual(result["aida_compliance_score"], 1.0)
        self.assertEqual(result["status"], "CONVERSION_READY")

    def test_audit_aida_framework_fail(self):
        text = "We have a building. It's okay. Contact us."
        result = self.copy.audit_aida_framework(text)
        self.assertLess(result["aida_compliance_score"], 0.75)
        self.assertEqual(result["status"], "WEAK_STRUCTURE")

    def test_score_hook_physics_high(self):
        text = "Are you tired of ordinary living?\nJoin the elite 1% today."
        result = self.copy.score_hook_physics(text)
        self.assertGreaterEqual(result["hook_efficiency"], 0.6)
        self.assertEqual(result["scroll_stop_prob"], "HIGH")

    def test_audit_information_density_omega(self):
        text = "Direct investment in New Cairo real estate projects yields high growth."
        result = self.copy.audit_information_density(text)
        self.assertGreaterEqual(result["density_score"], 0.9)
        self.assertTrue(result["is_omega_standard"])

    def test_generate_pas_structure(self):
        data = {"problem": "High rent", "agitation": "Losing equity", "solution": "Oasis Ownership"}
        result = self.copy.generate_pas_structure(data)
        self.assertIn("Losing equity", result["full_pas_copy"])
        self.assertEqual(result["status"], "DRAFT_GENERATED")

    def test_verify_omega_hook_density_pass(self):
        text = "Discover Oasis luxury.\nExclusive. Elite.\nActive now."
        result = self.copy.verify_omega_hook_density(text)
        self.assertTrue(result["is_omega_hook_compliant"])
        self.assertEqual(result["status"], "SCROLL_STOP_CERTIFIED")

if __name__ == '__main__':
    unittest.main()
