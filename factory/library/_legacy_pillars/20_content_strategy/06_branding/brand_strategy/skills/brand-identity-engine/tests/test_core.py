import unittest
from ..core import BrandIdentityEngine

class TestBrandIdentityEngine(unittest.TestCase):
    def setUp(self):
        self.skill = BrandIdentityEngine()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
