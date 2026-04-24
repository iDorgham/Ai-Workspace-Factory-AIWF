import unittest
from ..core import MobileHardwareAccess

class TestMobileHardwareAccess(unittest.TestCase):
    def setUp(self):
        self.skill = MobileHardwareAccess()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
