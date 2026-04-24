import unittest
from ..core import SddSpecWorkflow

class TestSddSpecWorkflow(unittest.TestCase):
    def setUp(self):
        self.skill = SddSpecWorkflow()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
