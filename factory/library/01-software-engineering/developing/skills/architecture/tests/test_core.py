import unittest
from ..core import Architecture

class TestArchitecture(unittest.TestCase):
    def setUp(self):
        self.skill = Architecture()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
