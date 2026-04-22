import unittest
from ..core import MistakePreventionSystem

class TestMistakePreventionSystem(unittest.TestCase):
    def setUp(self):
        self.skill = MistakePreventionSystem()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
