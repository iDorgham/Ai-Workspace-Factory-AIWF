import unittest
from ..core import PredictiveUnitEconomics

class TestPredictiveUnitEconomics(unittest.TestCase):
    def setUp(self):
        self.skill = PredictiveUnitEconomics()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
