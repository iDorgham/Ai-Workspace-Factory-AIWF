import unittest
from ..core import UnitEconomics

class TestUnitEconomics(unittest.TestCase):
    def setUp(self):
        self.skill = UnitEconomics()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
