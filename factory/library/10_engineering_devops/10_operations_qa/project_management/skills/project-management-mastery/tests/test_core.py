import unittest
from ..core import ProjectManagementMastery

class TestProjectManagementMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ProjectManagementMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
