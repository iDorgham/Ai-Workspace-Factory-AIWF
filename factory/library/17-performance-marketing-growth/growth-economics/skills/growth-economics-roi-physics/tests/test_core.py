import unittest
from ..core import GrowthEconomicsRoiPhysics

class TestGrowthEconomicsRoiPhysics(unittest.TestCase):
    def setUp(self):
        self.skill = GrowthEconomicsRoiPhysics()

    def test_run_creative_audit(self):
        self.assertTrue(self.skill.run_creative_audit({}))

if __name__ == '__main__':
    unittest.main()
