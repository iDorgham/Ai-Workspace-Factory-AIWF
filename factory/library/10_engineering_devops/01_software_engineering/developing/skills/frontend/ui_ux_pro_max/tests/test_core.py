import unittest
from ..core import UiUxProMax

class TestUiUxProMax(unittest.TestCase):
    def setUp(self):
        self.skill = UiUxProMax()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
