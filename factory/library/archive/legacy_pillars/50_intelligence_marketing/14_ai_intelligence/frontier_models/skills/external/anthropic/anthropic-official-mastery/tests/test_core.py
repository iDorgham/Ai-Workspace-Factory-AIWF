import unittest
from ..core import AnthropicOfficialMastery

class TestAnthropicOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = AnthropicOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
