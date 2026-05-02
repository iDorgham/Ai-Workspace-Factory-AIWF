import unittest
from ..core import FAndBOpsMastery

class TestFAndBOpsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = FAndBOpsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
