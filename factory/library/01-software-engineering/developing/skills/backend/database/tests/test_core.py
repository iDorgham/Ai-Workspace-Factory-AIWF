import unittest
from ..core import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.skill = Database()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
