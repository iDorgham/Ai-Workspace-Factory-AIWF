import unittest
from ..core import AdvancedSecurityAudit

class TestAdvancedSecurityAudit(unittest.TestCase):
    def setUp(self):
        self.audit = AdvancedSecurityAudit()

    def test_map_sensitive_flow(self):
        code = "const token = '123'; if (user.admin) { deleteUser(); }"
        result = self.audit.map_sensitive_flow(code)
        self.assertIn("token", result["entities_found"]["Auth"])
        self.assertEqual(result["privileged_transitions_detected"], 1)

    def test_verify_invariants_pass(self):
        state = {"user_balance": 100, "total_supply": 1000}
        invariants = ["user_balance >= 0", "total_supply <= 5000"]
        violations = self.audit.verify_invariants(state, invariants)
        self.assertEqual(len(violations), 0)

    def test_verify_invariants_fail(self):
        state = {"user_balance": -10}
        invariants = ["user_balance >= 0"]
        violations = self.audit.verify_invariants(state, invariants)
        self.assertEqual(len(violations), 1)
        self.assertIn("broken", violations[0])

    def test_audit_security_patterns(self):
        code = "try: do_thing() \nexcept: pass"
        result = self.audit.audit_security_patterns(code)
        self.assertFalse(result["is_standard"])
        self.assertGreater(result["findings"]["silent_failure"], 0)

if __name__ == '__main__':
    unittest.main()
