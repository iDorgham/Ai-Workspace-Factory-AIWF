import unittest
from ..core import EdgeCaseBoundaryTesting

class TestEdgeCaseBoundaryTesting(unittest.TestCase):
    def setUp(self):
        self.skill = EdgeCaseBoundaryTesting()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
