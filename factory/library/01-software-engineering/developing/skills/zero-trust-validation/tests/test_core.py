import unittest
from ..core import ZeroTrustValidation

class TestZeroTrustValidation(unittest.TestCase):
    def setUp(self):
        self.skill = ZeroTrustValidation()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
