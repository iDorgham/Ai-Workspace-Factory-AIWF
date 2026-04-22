import unittest
from ..core import DjMixingPerformance

class TestDjMixingPerformance(unittest.TestCase):
    def setUp(self):
        self.skill = DjMixingPerformance()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
