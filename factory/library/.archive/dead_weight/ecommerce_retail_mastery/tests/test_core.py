import unittest
from ..core import EcommerceRetailMastery

class TestEcommerceRetailMastery(unittest.TestCase):
    def setUp(self):
        self.skill = EcommerceRetailMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
