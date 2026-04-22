import unittest
from ..core import AutoOptimizationLoop

class TestAutoOptimizationLoop(unittest.TestCase):
    def setUp(self):
        self.skill = AutoOptimizationLoop()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
