import unittest
from ..core import DocsLintLinkCheck

class TestDocsLintLinkCheck(unittest.TestCase):
    def setUp(self):
        self.skill = DocsLintLinkCheck()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
