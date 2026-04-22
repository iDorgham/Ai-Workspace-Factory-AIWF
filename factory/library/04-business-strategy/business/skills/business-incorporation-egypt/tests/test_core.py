import unittest
from ..core import BusinessIncorporationEgypt

class TestBusinessIncorporationEgypt(unittest.TestCase):
    def setUp(self):
        self.skill = BusinessIncorporationEgypt()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
