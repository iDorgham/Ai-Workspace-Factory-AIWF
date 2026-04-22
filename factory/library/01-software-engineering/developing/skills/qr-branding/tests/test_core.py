import unittest
from ..core import QrBranding

class TestQrBranding(unittest.TestCase):
    def setUp(self):
        self.skill = QrBranding()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
