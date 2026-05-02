import unittest
from ..core import MultiPersonaBrandingMastery

class TestMultiPersonaBrandingMastery(unittest.TestCase):
    def setUp(self):
        self.skill = MultiPersonaBrandingMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
