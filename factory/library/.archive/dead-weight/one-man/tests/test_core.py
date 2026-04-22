import unittest
from ..core import OneMan

class TestOneMan(unittest.TestCase):
    def setUp(self):
        self.skill = OneMan()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
