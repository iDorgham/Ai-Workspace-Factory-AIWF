import unittest
from ..core import Testing

class TestTesting(unittest.TestCase):
    def setUp(self):
        self.skill = Testing()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
