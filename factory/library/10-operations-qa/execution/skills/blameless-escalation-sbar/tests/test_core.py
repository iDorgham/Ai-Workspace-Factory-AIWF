import unittest
from ..core import BlamelessEscalationSbar

class TestBlamelessEscalationSbar(unittest.TestCase):
    def setUp(self):
        self.skill = BlamelessEscalationSbar()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
