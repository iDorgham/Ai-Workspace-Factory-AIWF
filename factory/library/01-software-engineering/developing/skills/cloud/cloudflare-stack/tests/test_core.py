import unittest
from ..core import CloudflareStack

class TestCloudflareStack(unittest.TestCase):
    def setUp(self):
        self.skill = CloudflareStack()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
