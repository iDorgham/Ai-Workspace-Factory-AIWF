import unittest
from ..core import LegalTechMastery

class TestLegalTechMastery(unittest.TestCase):
    def setUp(self):
        self.skill = LegalTechMastery()

    def test_validate_compliance(self):
        self.assertTrue(self.skill.validate_compliance({}))

if __name__ == '__main__':
    unittest.main()
