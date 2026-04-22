import unittest
from ..core import ContentCreationMastery

class TestContentCreationMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ContentCreationMastery()

    def test_run_creative_audit(self):
        self.assertTrue(self.skill.run_creative_audit({}))

if __name__ == '__main__':
    unittest.main()
