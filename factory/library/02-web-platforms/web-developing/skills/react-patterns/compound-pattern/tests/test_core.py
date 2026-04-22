import unittest
from ..core import CompoundPattern

class TestCompoundPattern(unittest.TestCase):
    def setUp(self):
        self.skill = CompoundPattern()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
