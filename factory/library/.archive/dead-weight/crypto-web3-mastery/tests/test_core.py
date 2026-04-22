import unittest
from ..core import CryptoWeb3Mastery

class TestCryptoWeb3Mastery(unittest.TestCase):
    def setUp(self):
        self.skill = CryptoWeb3Mastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
