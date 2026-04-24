import unittest
from ..core import HallucinationContainment

class TestHallucinationContainment(unittest.TestCase):
    def setUp(self):
        self.skill = HallucinationContainment()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
