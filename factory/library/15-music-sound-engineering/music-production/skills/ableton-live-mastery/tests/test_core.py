import unittest
from ..core import AbletonLiveMastery

class TestAbletonLiveMastery(unittest.TestCase):
    def setUp(self):
        self.skill = AbletonLiveMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
