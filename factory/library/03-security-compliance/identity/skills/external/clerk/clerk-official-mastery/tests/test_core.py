import unittest
from ..core import ClerkOfficialMastery

class TestClerkOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ClerkOfficialMastery()

    def test_validate_compliance(self):
        self.assertTrue(self.skill.validate_compliance({}))

if __name__ == '__main__':
    unittest.main()
