import unittest
from ..core import GithubOfficialMastery

class TestGithubOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = GithubOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
