import unittest
from ..core import AiAvatarBrandingLogic

class TestAiAvatarBrandingLogic(unittest.TestCase):
    def setUp(self):
        self.skill = AiAvatarBrandingLogic()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
