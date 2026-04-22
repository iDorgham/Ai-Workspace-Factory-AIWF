import unittest
from ..core import TourismTravelMastery

class TestTourismTravelMastery(unittest.TestCase):
    def setUp(self):
        self.skill = TourismTravelMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
