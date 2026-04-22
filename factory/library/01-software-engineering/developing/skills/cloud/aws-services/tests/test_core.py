import unittest
from ..core import AwsServices

class TestAwsServices(unittest.TestCase):
    def setUp(self):
        self.skill = AwsServices()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
