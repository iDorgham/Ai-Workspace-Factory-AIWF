import unittest
from ..core import ViralLoopsMastery

class TestViralLoopsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ViralLoopsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
