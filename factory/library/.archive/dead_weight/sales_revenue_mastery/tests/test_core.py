import unittest
from ..core import SalesRevenueMastery

class TestSalesRevenueMastery(unittest.TestCase):
    def setUp(self):
        self.skill = SalesRevenueMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
