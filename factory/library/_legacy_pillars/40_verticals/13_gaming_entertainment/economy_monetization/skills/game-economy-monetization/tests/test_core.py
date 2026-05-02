import unittest
from ..core import GameEconomyMonetization

class TestGameEconomyMonetization(unittest.TestCase):
    def setUp(self):
        self.skill = GameEconomyMonetization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
