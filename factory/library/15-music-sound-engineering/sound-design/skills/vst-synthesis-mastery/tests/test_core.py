import unittest
from ..core import VstSynthesisMastery

class TestVstSynthesisMastery(unittest.TestCase):
    def setUp(self):
        self.skill = VstSynthesisMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
