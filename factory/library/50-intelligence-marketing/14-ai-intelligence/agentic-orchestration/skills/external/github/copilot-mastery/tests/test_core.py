import unittest
from ..core import CopilotMastery

class TestCopilotMastery(unittest.TestCase):
    def setUp(self):
        self.skill = CopilotMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
