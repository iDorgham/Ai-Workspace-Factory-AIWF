import unittest
from ..core import MetricsDrivenDecisions

class TestMetricsDrivenDecisions(unittest.TestCase):
    def setUp(self):
        self.skill = MetricsDrivenDecisions()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
