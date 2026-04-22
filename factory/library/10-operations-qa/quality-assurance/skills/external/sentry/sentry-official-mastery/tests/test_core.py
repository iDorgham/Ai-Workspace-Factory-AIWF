import unittest
from ..core import SentryOfficialMastery

class TestSentryOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.sentry = SentryOfficialMastery()

    def test_audit_error_fingerprinting_custom(self):
        report = {"type": "DatabaseError", "fingerprint": ["db-conn-fail", "main-db"]}
        result = self.sentry.audit_error_fingerprinting(report)
        self.assertTrue(result["has_custom_fingerprint"])
        self.assertTrue(result["is_optimized"])

    def test_audit_error_fingerprinting_generic_fail(self):
        report = {"type": "DatabaseError", "fingerprint": []} # Generic for critical DB error
        result = self.sentry.audit_error_fingerprinting(report)
        self.assertFalse(result["is_optimized"])
        self.assertIn("Implement custom fingerprinting", result["recommendation"])

    def test_validate_tracing_thresholds_healthy(self):
        stats = {"lcp": 1200.0, "fid": 45.0}
        result = self.sentry.validate_tracing_thresholds(stats)
        self.assertTrue(result["is_tracing_compliant"])
        self.assertEqual(result["status"], "HEALTHY")

    def test_validate_tracing_thresholds_degraded(self):
        stats = {"lcp": 3000.0} # LCP > 2.5s
        result = self.sentry.validate_tracing_thresholds(stats)
        self.assertFalse(result["is_tracing_compliant"])
        self.assertEqual(result["status"], "DEGRADED")

    def test_verify_tag_depth_complete(self):
        tags = {"environment": "prod", "release": "1.0.1", "server_name": "worker-1"}
        result = self.sentry.verify_tag_depth(tags)
        self.assertTrue(result["is_context_rich"])

    def test_verify_tag_depth_missing(self):
        tags = {"environment": "prod"}
        result = self.sentry.verify_tag_depth(tags)
        self.assertFalse(result["is_context_rich"])
        self.assertEqual(len(result["missing_tags"]), 2)

if __name__ == '__main__':
    unittest.main()
