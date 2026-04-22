import unittest
from ..core import GodotMastery

class TestGodotMastery(unittest.TestCase):
    def setUp(self):
        self.skill = GodotMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
