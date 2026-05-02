import unittest
from ..core import CliLimits

class TestCliLimits(unittest.TestCase):
    def setUp(self):
        self.skill = CliLimits()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
