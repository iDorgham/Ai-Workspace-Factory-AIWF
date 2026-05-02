import unittest
from ..core import StripeOfficialMastery

class TestStripeOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = StripeOfficialMastery()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
