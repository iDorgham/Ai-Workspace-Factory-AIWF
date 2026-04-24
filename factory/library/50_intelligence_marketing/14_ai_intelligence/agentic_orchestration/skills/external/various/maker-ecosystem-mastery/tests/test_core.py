import unittest
from ..core import MakerEcosystemMastery

class TestMakerEcosystemMastery(unittest.TestCase):
    def setUp(self):
        self.skill = MakerEcosystemMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
