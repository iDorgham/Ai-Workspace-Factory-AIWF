import unittest
from ..core import Security

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.skill = Security()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
