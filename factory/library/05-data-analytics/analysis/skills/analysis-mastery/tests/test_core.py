import unittest
from ..core import AnalysisMastery

class TestAnalysisMastery(unittest.TestCase):
    def setUp(self):
        self.skill = AnalysisMastery()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
