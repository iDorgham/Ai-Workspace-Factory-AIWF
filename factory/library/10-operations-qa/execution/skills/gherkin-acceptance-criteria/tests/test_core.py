import unittest
from ..core import GherkinAcceptanceCriteria

class TestGherkinAcceptanceCriteria(unittest.TestCase):
    def setUp(self):
        self.skill = GherkinAcceptanceCriteria()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
