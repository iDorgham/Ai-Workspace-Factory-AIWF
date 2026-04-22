import unittest
from ..core import IncrementalBuildStrategy

class TestIncrementalBuildStrategy(unittest.TestCase):
    def setUp(self):
        self.skill = IncrementalBuildStrategy()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
