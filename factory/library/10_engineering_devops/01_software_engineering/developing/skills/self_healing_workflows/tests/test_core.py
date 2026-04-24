import unittest
from ..core import SelfHealingWorkflows

class TestSelfHealingWorkflows(unittest.TestCase):
    def setUp(self):
        self.skill = SelfHealingWorkflows()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
