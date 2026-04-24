import unittest
from ..core import NeonPostgres

class TestNeonPostgres(unittest.TestCase):
    def setUp(self):
        self.skill = NeonPostgres()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
