import unittest
from ..core import PlaywrightE2E

class TestPlaywrightE2E(unittest.TestCase):
    def setUp(self):
        self.skill = PlaywrightE2E()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
