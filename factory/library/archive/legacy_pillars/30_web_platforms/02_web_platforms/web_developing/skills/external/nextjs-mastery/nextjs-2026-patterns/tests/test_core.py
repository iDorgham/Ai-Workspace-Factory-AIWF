import unittest
from ..core import Nextjs2026Patterns

class TestNextjs2026Patterns(unittest.TestCase):
    def setUp(self):
        self.skill = Nextjs2026Patterns()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
