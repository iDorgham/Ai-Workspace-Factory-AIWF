import unittest
from ..core import TestingMastery

class TestTestingMastery(unittest.TestCase):
    def setUp(self):
        self.testing = TestingMastery()

    def test_audit_quality_gate(self):
        self.assertTrue(self.testing.audit_quality_gate({"failures": 0, "errors": 0}))
        self.assertFalse(self.testing.audit_quality_gate({"failures": 1, "errors": 0}))

    def test_analyze_coverage(self):
        self.assertEqual(self.testing.analyze_coverage({"total": 88.0}), 88.0)

if __name__ == '__main__':
    unittest.main()
