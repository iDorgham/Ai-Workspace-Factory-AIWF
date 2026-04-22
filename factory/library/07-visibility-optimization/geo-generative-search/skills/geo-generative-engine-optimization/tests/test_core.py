import unittest
from ..core import GeoGenerativeEngineOptimization

class TestGeoGenerativeEngineOptimization(unittest.TestCase):
    def setUp(self):
        self.skill = GeoGenerativeEngineOptimization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
