import unittest
from ..core import UnrealCppMastery

class TestUnrealCppMastery(unittest.TestCase):
    def setUp(self):
        self.skill = UnrealCppMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
