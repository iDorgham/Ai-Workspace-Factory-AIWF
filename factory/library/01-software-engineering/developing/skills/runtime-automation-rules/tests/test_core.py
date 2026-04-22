import unittest
from ..core import RuntimeAutomationRules

class TestRuntimeAutomationRules(unittest.TestCase):
    def setUp(self):
        self.skill = RuntimeAutomationRules()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
