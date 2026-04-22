import unittest
from ..core import BilingualNextJSPerformance

class TestBilingualNextJSPerformance(unittest.TestCase):
    def setUp(self):
        self.perf = BilingualNextJSPerformance()

    def test_audit_logical_properties_pass(self):
        css = ".element { padding-inline-start: 10px; margin-inline-end: 5px; text-align: start; }"
        result = self.perf.audit_logical_properties(css)
        self.assertTrue(result["is_bilingual_compliant"])
        self.assertEqual(len(result["violations"]), 0)

    def test_audit_logical_properties_fail(self):
        css = ".element { padding-left: 10px; text-align: right; }"
        result = self.perf.audit_logical_properties(css)
        self.assertFalse(result["is_bilingual_compliant"])
        self.assertIn("Hardcoded directional property", result["violations"][0])

    def test_audit_font_subsetting_unoptimized(self):
        config = {"full_size_kb": 600, "is_subsetted": False}
        result = self.perf.audit_font_subsetting(config)
        self.assertFalse(result["is_optimized"])
        self.assertEqual(result["potential_savings_kb"], 300.0)

    def test_verify_regional_edge_caching_fast(self):
        stats = {"UAE": 85.0, "KSA": 110.0, "Egypt": 45.0}
        result = self.perf.verify_regional_edge_caching(stats)
        self.assertTrue(result["is_regionally_optimized"])

    def test_verify_regional_edge_caching_slow(self):
        stats = {"UAE": 250.0} # Threshold 200
        result = self.perf.verify_regional_edge_caching(stats)
        self.assertFalse(result["is_regionally_optimized"])

if __name__ == '__main__':
    unittest.main()
