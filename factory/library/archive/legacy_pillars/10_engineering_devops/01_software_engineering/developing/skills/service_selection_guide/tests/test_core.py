import unittest
from ..core import ServiceSelectionGuide

class TestServiceSelectionGuide(unittest.TestCase):
    def setUp(self):
        self.skill = ServiceSelectionGuide()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
