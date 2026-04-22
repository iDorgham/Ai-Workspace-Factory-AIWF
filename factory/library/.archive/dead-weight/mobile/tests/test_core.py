import unittest
from ..core import Mobile

class TestMobile(unittest.TestCase):
    def setUp(self):
        self.skill = Mobile()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
