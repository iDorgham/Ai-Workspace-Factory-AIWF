import unittest
from ..core import TechnicalSeoMastery

class TestTechnicalSeoMastery(unittest.TestCase):
    def setUp(self):
        self.skill = TechnicalSeoMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
