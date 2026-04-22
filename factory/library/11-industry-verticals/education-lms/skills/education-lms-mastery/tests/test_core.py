import unittest
from ..core import EducationLmsMastery

class TestEducationLmsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = EducationLmsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
