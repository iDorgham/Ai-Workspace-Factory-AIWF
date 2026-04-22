import unittest
from ..core import ContentSocialProduction

class TestContentSocialProduction(unittest.TestCase):
    def setUp(self):
        self.skill = ContentSocialProduction()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
