import unittest
from ..core import WrittenLeadgenBioMastery

class TestWrittenLeadgenBioMastery(unittest.TestCase):
    def setUp(self):
        self.skill = WrittenLeadgenBioMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
