import unittest
from ..core import PnpmVersionCatalogs

class TestPnpmVersionCatalogs(unittest.TestCase):
    def setUp(self):
        self.skill = PnpmVersionCatalogs()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
