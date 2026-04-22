import unittest
from ..core import PrismaAdvanced

class TestPrismaAdvanced(unittest.TestCase):
    def setUp(self):
        self.skill = PrismaAdvanced()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
