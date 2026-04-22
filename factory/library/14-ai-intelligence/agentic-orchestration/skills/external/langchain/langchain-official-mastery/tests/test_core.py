import unittest
from ..core import LangchainOfficialMastery

class TestLangchainOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = LangchainOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
