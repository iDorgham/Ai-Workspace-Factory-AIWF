import unittest
from ..core import AssetOptimization

class TestAssetOptimization(unittest.TestCase):
    def setUp(self):
        self.skill = AssetOptimization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
