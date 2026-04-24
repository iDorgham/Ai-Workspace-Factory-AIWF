import unittest
from ..core import BilingualAdLocalizationEnar

class TestBilingualAdLocalizationEnar(unittest.TestCase):
    def setUp(self):
        self.skill = BilingualAdLocalizationEnar()

    def test_run_creative_audit(self):
        self.assertTrue(self.skill.run_creative_audit({}))

if __name__ == '__main__':
    unittest.main()
