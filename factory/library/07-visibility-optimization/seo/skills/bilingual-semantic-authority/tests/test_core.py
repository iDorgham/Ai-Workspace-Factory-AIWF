import unittest
from ..core import BilingualSemanticAuthority

class TestBilingualSemanticAuthority(unittest.TestCase):
    def setUp(self):
        self.seo = BilingualSemanticAuthority()

    def test_map_voice_intent_success(self):
        result = self.seo.map_voice_intent("شقق قريبة من المترو")
        self.assertTrue(result["is_mapped"])
        self.assertEqual(result["semantic_mapping"]["intent"], "Commuter Accessibility")

    def test_map_voice_intent_generic(self):
        result = self.seo.map_voice_intent("unknown query")
        self.assertFalse(result["is_mapped"])

    def test_audit_hreflang_parity_pass(self):
        pages = [
            {"url": "/en", "alternates": {"ar-ae": "/ar", "en-ae": "/en"}},
            {"url": "/ar", "alternates": {"ar-ae": "/ar", "en-ae": "/en"}}
        ]
        result = self.seo.audit_hreflang_parity(pages)
        self.assertTrue(result["is_hreflang_compliant"])

    def test_audit_hreflang_parity_fail(self):
        pages = [{"url": "/en", "alternates": {"en-ae": "/en"}}] # Missing ar-ae
        result = self.seo.audit_hreflang_parity(pages)
        self.assertFalse(result["is_hreflang_compliant"])

    def test_validate_topic_clusters(self):
        kws = ["Exclusive mansion", "Off-plan projects", "Generic keyword"]
        result = self.seo.validate_topic_clusters(kws)
        self.assertIn("Exclusive mansion", result["clusters"]["Luxury"])
        self.assertIn("Off-plan projects", result["clusters"]["Off-plan"])
        self.assertEqual(result["unmapped_count"], 1)

    def test_audit_rtl_semantic_alignment_omega(self):
        segments = ["هذا عقار فاخر في دبي", "This is a luxury property"]
        result = self.seo.audit_rtl_semantic_alignment(segments)
        self.assertGreater(result["average_rtl_alignment"], 0.4)
        self.assertEqual(result["detailed_audit"][0]["type"], "FUSHA_SEO")

if __name__ == '__main__':
    unittest.main()
