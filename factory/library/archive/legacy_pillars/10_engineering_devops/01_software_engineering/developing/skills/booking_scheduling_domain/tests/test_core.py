import unittest
from ..core import BookingSchedulingDomain

class TestBookingSchedulingDomain(unittest.TestCase):
    def setUp(self):
        self.skill = BookingSchedulingDomain()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
