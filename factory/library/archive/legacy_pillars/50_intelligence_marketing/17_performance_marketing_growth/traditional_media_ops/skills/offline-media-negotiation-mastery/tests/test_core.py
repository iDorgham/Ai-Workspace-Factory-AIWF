import unittest
from ..core import OfflineMediaNegotiationMastery

class TestOfflineMediaNegotiationMastery(unittest.TestCase):
    def setUp(self):
        self.skill = OfflineMediaNegotiationMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
