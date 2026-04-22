import unittest
from ..core import IosAppleMastery

class TestIosAppleMastery(unittest.TestCase):
    def setUp(self):
        self.skill = IosAppleMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
