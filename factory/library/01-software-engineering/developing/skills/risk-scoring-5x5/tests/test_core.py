import unittest
from ..core import RiskScoring5X5

class TestRiskScoring5X5(unittest.TestCase):
    def setUp(self):
        self.skill = RiskScoring5X5()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
