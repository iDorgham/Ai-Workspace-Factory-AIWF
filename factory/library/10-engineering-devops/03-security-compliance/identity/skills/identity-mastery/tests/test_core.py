import unittest
from ..core import IdentityMastery

class TestIdentityMastery(unittest.TestCase):
    def setUp(self):
        self.skill = IdentityMastery()

    def test_validate_compliance(self):
        self.assertTrue(self.skill.validate_compliance({}))

if __name__ == '__main__':
    unittest.main()
