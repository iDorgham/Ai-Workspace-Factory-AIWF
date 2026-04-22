import unittest
from ..core import CyberSecurityMastery

class TestCyberSecurityMastery(unittest.TestCase):
    def setUp(self):
        self.security = CyberSecurityMastery()

    def test_audit_secure_design_secure(self):
        config = {
            "rbac_active": True,
            "is_root_run": False,
            "input_validation_layer": True,
            "storage_encrypted": True,
            "mtls_active": True
        }
        result = self.security.audit_secure_design(config)
        self.assertEqual(result["compliance_score"], 1.0)
        self.assertEqual(result["status"], "SECURE")

    def test_audit_secure_design_vulnerable(self):
        config = {"is_root_run": True, "storage_encrypted": False}
        result = self.security.audit_secure_design(config)
        self.assertLess(result["compliance_score"], 0.75)
        self.assertEqual(result["status"], "VULNERABLE")

    def test_calculate_threat_score_critical(self):
        manifest = "const secret = 'hardcoded_key'; eval(user_input);"
        result = self.security.calculate_threat_score(manifest)
        self.assertEqual(result["vulnerability_count"], 2)
        self.assertEqual(result["threat_impact"], "CRITICAL")

    def test_validate_auth_physics_hardened(self):
        auth = {"mfa_active": True, "jwt_refresh_rotation": True, "rate_limit_enabled": True}
        result = self.security.validate_auth_physics(auth)
        self.assertTrue(result["is_launch_ready"])
        self.assertEqual(result["recommendation"], "HARDENED")

if __name__ == '__main__':
    unittest.main()
