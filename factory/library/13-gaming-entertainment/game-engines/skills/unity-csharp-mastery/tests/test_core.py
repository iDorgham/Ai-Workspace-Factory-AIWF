import unittest
from ..core import UnityCsharpMastery

class TestUnityCsharpMastery(unittest.TestCase):
    def setUp(self):
        self.skill = UnityCsharpMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
