import unittest
from ..core import TurborepoMastery

class TestTurborepoMastery(unittest.TestCase):
    def setUp(self):
        self.skill = TurborepoMastery()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
