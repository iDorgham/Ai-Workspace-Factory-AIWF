import unittest
from ..core import UpstashIntegration

class TestUpstashIntegration(unittest.TestCase):
    def setUp(self):
        self.skill = UpstashIntegration()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
