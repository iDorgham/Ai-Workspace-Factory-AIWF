import unittest
from ..core import EdgePatterns

class TestEdgePatterns(unittest.TestCase):
    def setUp(self):
        self.skill = EdgePatterns()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
