import unittest
from ..core import QrCrypto

class TestQrCrypto(unittest.TestCase):
    def setUp(self):
        self.skill = QrCrypto()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
