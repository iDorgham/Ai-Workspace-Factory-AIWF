import unittest
from ..core import CliMemory

class TestCliMemory(unittest.TestCase):
    def setUp(self):
        self.skill = CliMemory()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
