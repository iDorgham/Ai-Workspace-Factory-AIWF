import unittest
from ..core import AiUiPatterns

class TestAiUiPatterns(unittest.TestCase):
    def setUp(self):
        self.skill = AiUiPatterns()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
