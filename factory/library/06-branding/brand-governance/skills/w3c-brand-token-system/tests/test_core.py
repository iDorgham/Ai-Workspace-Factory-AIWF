import unittest
from ..core import W3CBrandTokenSystem

class TestW3CBrandTokenSystem(unittest.TestCase):
    def setUp(self):
        self.skill = W3CBrandTokenSystem()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
