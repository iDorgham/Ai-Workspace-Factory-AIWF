import unittest
from ..core import AccessibilityWcag

class TestAccessibilityWcag(unittest.TestCase):
    def setUp(self):
        self.skill = AccessibilityWcag()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
