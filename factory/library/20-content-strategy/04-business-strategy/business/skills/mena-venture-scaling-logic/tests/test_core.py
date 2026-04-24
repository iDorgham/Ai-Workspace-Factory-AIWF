import unittest
from ..core import MenaVentureScalingLogic

class TestMenaVentureScalingLogic(unittest.TestCase):
    def setUp(self):
        self.skill = MenaVentureScalingLogic()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
