import unittest
from ..core import RailwayDeployment

class TestRailwayDeployment(unittest.TestCase):
    def setUp(self):
        self.skill = RailwayDeployment()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
