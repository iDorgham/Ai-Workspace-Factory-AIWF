import unittest
from ..core import MotionAnimationSystem

class TestMotionAnimationSystem(unittest.TestCase):
    def setUp(self):
        self.skill = MotionAnimationSystem()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
