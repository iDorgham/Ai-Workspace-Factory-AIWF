import unittest
from ..core import Vercel

class TestVercel(unittest.TestCase):
    def setUp(self):
        self.skill = Vercel()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
