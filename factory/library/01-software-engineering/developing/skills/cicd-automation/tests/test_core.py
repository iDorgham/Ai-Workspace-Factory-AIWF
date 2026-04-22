import unittest
from ..core import CicdAutomation

class TestCicdAutomation(unittest.TestCase):
    def setUp(self):
        self.skill = CicdAutomation()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
