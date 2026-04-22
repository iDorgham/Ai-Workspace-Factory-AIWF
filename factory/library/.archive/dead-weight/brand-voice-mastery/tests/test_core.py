import unittest
from ..core import BrandVoiceMastery

class TestBrandVoiceMastery(unittest.TestCase):
    def setUp(self):
        self.skill = BrandVoiceMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
