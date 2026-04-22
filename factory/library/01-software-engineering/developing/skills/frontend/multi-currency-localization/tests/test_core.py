import unittest
from ..core import MultiCurrencyLocalization

class TestMultiCurrencyLocalization(unittest.TestCase):
    def setUp(self):
        self.skill = MultiCurrencyLocalization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
