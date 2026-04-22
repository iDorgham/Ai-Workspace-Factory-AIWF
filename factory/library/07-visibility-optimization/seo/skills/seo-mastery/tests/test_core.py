import unittest
import json
from ..core import SeoMastery

class TestSeoMastery(unittest.TestCase):
    def setUp(self):
        self.seo = SeoMastery()

    def test_run_technical_audit_healthy(self):
        data = {
            "core_web_vitals": {"lcp": 1200, "fid": 50, "cls": 0.05},
            "is_indexable": True
        }
        result = self.seo.run_technical_audit(data)
        self.assertTrue(result["is_standard"])
        self.assertEqual(len(result["violations"]), 0)

    def test_run_technical_audit_violations(self):
        data = {
            "core_web_vitals": {"lcp": 3000, "fid": 150, "cls": 0.2},
            "is_indexable": False
        }
        result = self.seo.run_technical_audit(data)
        self.assertFalse(result["is_standard"])
        self.assertEqual(len(result["violations"]), 3)

    def test_generate_bilingual_schema(self):
        entity = {
            "name_en": "Sovereign",
            "name_ar": "غاليريا",
            "desc_en": "High-density factory."
        }
        schema_str = self.seo.generate_bilingual_schema(entity)
        schema = json.loads(schema_str)
        self.assertEqual(schema["name"]["@value"], "Sovereign")
        self.assertEqual(schema["alternateName"]["@value"], "غاليريا")

    def test_validate_rtl_search_intent(self):
        keywords = ["Real Estate", "عقارات دبي", "PropTech"]
        opt = self.seo.validate_rtl_search_intent(keywords)
        self.assertEqual(len(opt), 1)
        self.assertIn("عقارات دبي", opt[0])

    def test_calculate_gvi_score_omega(self):
        data = {"technical_compliance": 98.0, "serp_presence": 96.0, "indexing_depth": 95.0}
        result = self.seo.calculate_gvi_score(data)
        self.assertTrue(result["is_omega_certified"])
        self.assertEqual(result["tier"], "💎 OMEGA")

    def test_generate_bilingual_metadata(self):
        context = {"title_en": "Luxury Real Estate", "title_ar": "عقارات فاخرة"}
        result = self.seo.generate_bilingual_metadata(context)
        self.assertIn("عقارات فاخرة", result["meta_title"])
        self.assertIn("Luxury Real Estate", result["meta_title"])
        self.assertEqual(result["status"], "BILINGUAL_SYNCED")

if __name__ == '__main__':
    unittest.main()
