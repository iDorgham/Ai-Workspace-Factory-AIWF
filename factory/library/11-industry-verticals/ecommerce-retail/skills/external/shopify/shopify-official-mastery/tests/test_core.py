import unittest
from ..core import ShopifyOfficialMastery

class TestShopifyOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ShopifyOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
