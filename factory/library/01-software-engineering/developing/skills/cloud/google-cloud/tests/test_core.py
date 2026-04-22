import unittest
from ..core import GoogleCloud

class TestGoogleCloud(unittest.TestCase):
    def setUp(self):
        self.skill = GoogleCloud()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
