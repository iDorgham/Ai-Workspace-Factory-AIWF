import unittest
from ..core import RbacPermissionSystem

class TestRbacPermissionSystem(unittest.TestCase):
    def setUp(self):
        self.skill = RbacPermissionSystem()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
