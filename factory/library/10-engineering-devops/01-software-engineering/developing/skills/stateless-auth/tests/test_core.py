import unittest
from ..core import StatelessAuth

class TestStatelessAuth(unittest.TestCase):
    def setUp(self):
        self.skill = StatelessAuth()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
