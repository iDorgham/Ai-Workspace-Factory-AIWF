import unittest
from ..core import HospitalClinicMastery

class TestHospitalClinicMastery(unittest.TestCase):
    def setUp(self):
        self.skill = HospitalClinicMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
