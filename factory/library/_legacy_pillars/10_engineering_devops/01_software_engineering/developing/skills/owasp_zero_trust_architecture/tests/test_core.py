import unittest
from ..core import OwaspZeroTrustArchitecture

class TestOwaspZeroTrustArchitecture(unittest.TestCase):
    def setUp(self):
        self.skill = OwaspZeroTrustArchitecture()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
