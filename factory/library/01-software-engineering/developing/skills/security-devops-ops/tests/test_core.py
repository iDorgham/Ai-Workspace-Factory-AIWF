import unittest
from ..core import SecurityDevopsOps

class TestSecurityDevopsOps(unittest.TestCase):
    def setUp(self):
        self.skill = SecurityDevopsOps()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
