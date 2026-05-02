import unittest
from ..core import VercelOfficialMastery

class TestVercelOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = VercelOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
