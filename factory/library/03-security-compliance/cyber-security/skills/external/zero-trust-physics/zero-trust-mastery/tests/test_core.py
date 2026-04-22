import unittest
from ..core import ZeroTrustMastery

class TestZeroTrustMastery(unittest.TestCase):
    def setUp(self):
        self.zt = ZeroTrustMastery()

    def test_audit_microsegmentation_pass(self):
        traffic = [
            {"service_id": "api-1", "source_type": "internal", "has_valid_identity_token": True},
            {"service_id": "web-1", "source_type": "external", "has_valid_identity_token": True}
        ]
        result = self.zt.audit_microsegmentation(traffic)
        self.assertTrue(result["is_microsegmented"])
        self.assertEqual(result["status"], "HARDENED")

    def test_audit_microsegmentation_fail(self):
        traffic = [
            {"service_id": "db-1", "source_type": "internal", "has_valid_identity_token": False}
        ]
        result = self.zt.audit_microsegmentation(traffic)
        self.assertFalse(result["is_microsegmented"])
        self.assertEqual(len(result["violations"]), 1)

    def test_validate_jit_escalation_valid(self):
        req = {"expiry_minutes": 30, "is_scoped_to_task": True, "has_peer_approval": True}
        result = self.zt.validate_jit_escalation(req)
        self.assertTrue(result["is_jit_compliant"])

    def test_validate_jit_escalation_invalid_ttl(self):
        req = {"expiry_minutes": 120, "is_scoped_to_task": True, "has_peer_approval": True}
        result = self.zt.validate_jit_escalation(req)
        self.assertFalse(result["is_jit_compliant"])

    def test_audit_mtls_conduits_complete(self):
        stats = {
            "high_risk_paths": ["db-to-finance", "api-to-vault"],
            "mtls_enabled_paths": ["db-to-finance", "api-to-vault"]
        }
        result = self.zt.audit_mtls_conduits(stats)
        self.assertTrue(result["is_mtls_enforced"])
        self.assertEqual(result["compliance_percentage"], 100.0)

    def test_audit_mtls_conduits_partial(self):
        stats = {
            "high_risk_paths": ["db-to-finance", "api-to-vault"],
            "mtls_enabled_paths": ["db-to-finance"]
        }
        result = self.zt.audit_mtls_conduits(stats)
        self.assertFalse(result["is_mtls_enforced"])
        self.assertEqual(len(result["missing_conduits"]), 1)

if __name__ == '__main__':
    unittest.main()
