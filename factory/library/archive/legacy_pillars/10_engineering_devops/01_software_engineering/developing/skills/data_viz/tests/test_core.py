import unittest
from ..core import DataViz

class TestDataViz(unittest.TestCase):
    def setUp(self):
        self.skill = DataViz()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
