import unittest
from ..core import HighDensityCopywritingProtocols

class TestHighDensityCopywritingProtocols(unittest.TestCase):
    def setUp(self):
        self.skill = HighDensityCopywritingProtocols()

    def test_run_creative_audit(self):
        self.assertTrue(self.skill.run_creative_audit({}))

if __name__ == '__main__':
    unittest.main()
