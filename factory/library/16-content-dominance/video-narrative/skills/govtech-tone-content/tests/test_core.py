import unittest
from ..core import GovtechToneContent

class TestGovtechToneContent(unittest.TestCase):
    def setUp(self):
        self.skill = GovtechToneContent()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
