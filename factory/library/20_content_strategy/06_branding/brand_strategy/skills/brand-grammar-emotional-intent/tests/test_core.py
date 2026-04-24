import unittest
from ..core import BrandGrammarEmotionalIntent

class TestBrandGrammarEmotionalIntent(unittest.TestCase):
    def setUp(self):
        self.skill = BrandGrammarEmotionalIntent()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
