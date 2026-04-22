import unittest
from ..core import BackendMastery

class TestBackendMastery(unittest.TestCase):
    def setUp(self):
        self.backend = BackendMastery()

    def test_audit_latency_profile(self):
        result = self.backend.audit_latency_profile([])
        self.assertIn("p95_latency", result)

    def test_check_security_hardening(self):
        middleware = ["helmet-config", "cors-setup", "rate-limiter"]
        self.assertTrue(self.backend.check_security_hardening(middleware))
        self.assertFalse(self.backend.check_security_hardening(["just-cors"]))

if __name__ == '__main__':
    unittest.main()
