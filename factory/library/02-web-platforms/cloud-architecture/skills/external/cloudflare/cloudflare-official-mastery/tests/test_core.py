import unittest
from ..core import CloudflareOfficialMastery

class TestCloudflareOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.skill = CloudflareOfficialMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
