import unittest
from ..core import PreFlightChecklist

class TestPreFlightChecklist(unittest.TestCase):
    def setUp(self):
        self.skill = PreFlightChecklist()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
