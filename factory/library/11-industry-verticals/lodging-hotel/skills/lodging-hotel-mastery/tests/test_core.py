import unittest
from ..core import LodgingHotelMastery

class TestLodgingHotelMastery(unittest.TestCase):
    def setUp(self):
        self.skill = LodgingHotelMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
