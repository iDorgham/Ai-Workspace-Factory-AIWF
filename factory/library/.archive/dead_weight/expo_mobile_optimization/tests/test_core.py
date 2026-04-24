import unittest
from ..core import ExpoMobileOptimization

class TestExpoMobileOptimization(unittest.TestCase):
    def setUp(self):
        self.skill = ExpoMobileOptimization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
