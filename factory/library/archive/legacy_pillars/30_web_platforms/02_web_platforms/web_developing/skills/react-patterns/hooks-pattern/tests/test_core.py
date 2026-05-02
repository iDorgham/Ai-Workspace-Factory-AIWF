import unittest
from ..core import HooksPattern

class TestHooksPattern(unittest.TestCase):
    def setUp(self):
        self.skill = HooksPattern()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
