import unittest
from ..core import AgencyCreativeMastery

class TestAgencyCreativeMastery(unittest.TestCase):
    def setUp(self):
        self.skill = AgencyCreativeMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
