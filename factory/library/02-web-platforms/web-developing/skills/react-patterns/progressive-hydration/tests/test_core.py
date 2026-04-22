import unittest
from ..core import ProgressiveHydration

class TestProgressiveHydration(unittest.TestCase):
    def setUp(self):
        self.skill = ProgressiveHydration()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
