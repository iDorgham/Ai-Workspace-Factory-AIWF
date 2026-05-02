import unittest
from ..core import SocialContentViralLoops

class TestSocialContentViralLoops(unittest.TestCase):
    def setUp(self):
        self.skill = SocialContentViralLoops()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
