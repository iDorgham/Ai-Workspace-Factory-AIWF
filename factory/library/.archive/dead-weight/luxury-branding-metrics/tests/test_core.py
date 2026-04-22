import unittest
from ..core import LuxuryBrandingMetrics

class TestLuxuryBrandingMetrics(unittest.TestCase):
    def setUp(self):
        self.skill = LuxuryBrandingMetrics()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
