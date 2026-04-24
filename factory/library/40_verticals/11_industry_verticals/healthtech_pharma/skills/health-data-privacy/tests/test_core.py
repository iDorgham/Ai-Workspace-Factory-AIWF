import unittest
from ..core import HealthDataPrivacy

class TestHealthDataPrivacy(unittest.TestCase):
    def setUp(self):
        self.skill = HealthDataPrivacy()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
