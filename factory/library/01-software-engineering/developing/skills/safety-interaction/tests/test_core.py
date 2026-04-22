import unittest
from ..core import SafetyInteraction

class TestSafetyInteraction(unittest.TestCase):
    def setUp(self):
        self.skill = SafetyInteraction()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
