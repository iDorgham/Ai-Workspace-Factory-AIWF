import unittest
from ..core import Strategist

class TestStrategist(unittest.TestCase):
    def setUp(self):
        self.skill = Strategist()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
