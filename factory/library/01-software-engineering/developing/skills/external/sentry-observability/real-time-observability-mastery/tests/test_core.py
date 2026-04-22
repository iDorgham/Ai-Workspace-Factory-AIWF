import unittest
from ..core import RealTimeObservabilityMastery

class TestRealTimeObservabilityMastery(unittest.TestCase):
    def setUp(self):
        self.skill = RealTimeObservabilityMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
