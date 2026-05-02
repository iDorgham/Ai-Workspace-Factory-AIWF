import unittest
from ..core import HocPattern

class TestHocPattern(unittest.TestCase):
    def setUp(self):
        self.skill = HocPattern()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
