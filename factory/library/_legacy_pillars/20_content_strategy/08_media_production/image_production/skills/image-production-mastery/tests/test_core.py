import unittest
from ..core import ImageProductionMastery

class TestImageProductionMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ImageProductionMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
