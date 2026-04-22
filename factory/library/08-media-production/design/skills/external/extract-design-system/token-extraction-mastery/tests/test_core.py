import unittest
from ..core import TokenExtractionMastery

class TestTokenExtractionMastery(unittest.TestCase):
    def setUp(self):
        self.skill = TokenExtractionMastery()

    def test_run_operational_audit(self):
        self.assertTrue(self.skill.run_operational_audit({}))

if __name__ == '__main__':
    unittest.main()
