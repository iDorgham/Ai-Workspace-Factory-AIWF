import unittest
from ..core import HighDensityContentMastery

class TestHighDensityContentMastery(unittest.TestCase):
    def setUp(self):
        self.skill = HighDensityContentMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
