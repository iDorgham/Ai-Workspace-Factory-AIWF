import unittest
from ..core import DevelopingMastery

class TestDevelopingMastery(unittest.TestCase):
    def setUp(self):
        self.skill = DevelopingMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
