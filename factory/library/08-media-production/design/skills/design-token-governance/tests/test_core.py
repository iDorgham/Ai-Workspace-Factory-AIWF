import unittest
from ..core import DesignTokenGovernance

class TestDesignTokenGovernance(unittest.TestCase):
    def setUp(self):
        self.skill = DesignTokenGovernance()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
