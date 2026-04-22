import unittest
from ..core import MenaConstitutionalBoundaries

class TestMenaConstitutionalBoundaries(unittest.TestCase):
    def setUp(self):
        self.skill = MenaConstitutionalBoundaries()

    def test_validate_compliance(self):
        self.assertTrue(self.skill.validate_compliance({}))

if __name__ == '__main__':
    unittest.main()
