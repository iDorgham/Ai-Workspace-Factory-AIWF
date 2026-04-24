import unittest
from ..core import SentryObservability

class TestSentryObservability(unittest.TestCase):
    def setUp(self):
        self.skill = SentryObservability()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
