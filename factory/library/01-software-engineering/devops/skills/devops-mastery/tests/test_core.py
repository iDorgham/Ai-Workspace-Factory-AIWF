import unittest
from ..core import DevopsMastery

class TestDevopsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = DevopsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
