import unittest
from ..core import MobileDesign

class TestMobileDesign(unittest.TestCase):
    def setUp(self):
        self.skill = MobileDesign()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
