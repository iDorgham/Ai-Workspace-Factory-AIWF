import unittest
from ..core import SupabaseOfficialMastery

class TestSupabaseOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.supabase = SupabaseOfficialMastery()

    def test_audit_rls_compliance_pass(self):
        schema = {"rls_enabled": True, "policies": ["authenticated_select"]}
        result = self.supabase.audit_rls_compliance(schema)
        self.assertTrue(result["is_rls_compliant"])
        self.assertEqual(result["status"], "APPROVED")

    def test_audit_rls_compliance_fail(self):
        schema = {"rls_enabled": False}
        result = self.supabase.audit_rls_compliance(schema)
        self.assertFalse(result["is_rls_compliant"])
        self.assertEqual(result["status"], "RLS_SECURITY_HOLD")

    def test_validate_regional_latency_localized(self):
        config = {"supabase_region": "me-central-1"}
        result = self.supabase.validate_regional_latency(config)
        self.assertTrue(result["is_localized"])
        self.assertEqual(result["latency_impact"], "OPTIMIZED")

    def test_audit_indexing_heuristics_omega(self):
        metrics = {"has_btree_index": True, "has_gin_index": True, "estimated_rows": 50000}
        result = self.supabase.audit_indexing_heuristics(metrics)
        self.assertTrue(result["is_query_optimized"])
        self.assertEqual(result["tier"], "OMEGA")

if __name__ == '__main__':
    unittest.main()
