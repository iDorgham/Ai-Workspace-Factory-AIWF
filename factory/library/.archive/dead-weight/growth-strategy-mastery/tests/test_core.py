import unittest
from ..core import GrowthStrategyMastery

class TestGrowthStrategyMastery(unittest.TestCase):
    def setUp(self):
        self.skill = GrowthStrategyMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
