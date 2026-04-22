import unittest
from ..core import ContextCompression

class TestContextCompression(unittest.TestCase):
    def setUp(self):
        self.skill = ContextCompression()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
