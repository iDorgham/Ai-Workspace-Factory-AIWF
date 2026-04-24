import unittest
from ..core import Vercel2026Architecture

class TestVercel2026Architecture(unittest.TestCase):
    def setUp(self):
        self.skill = Vercel2026Architecture()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
