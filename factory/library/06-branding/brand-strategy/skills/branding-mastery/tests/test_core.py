import unittest
from ..core import BrandingMastery

class TestBrandingMastery(unittest.TestCase):
    def setUp(self):
        self.skill = BrandingMastery()

    def test_run_operational_audit(self):
        self.assertTrue(self.skill.run_operational_audit({}))

if __name__ == '__main__':
    unittest.main()
