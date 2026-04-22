import unittest
from ..core import ExpoOfflineSync

class TestExpoOfflineSync(unittest.TestCase):
    def setUp(self):
        self.skill = ExpoOfflineSync()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
