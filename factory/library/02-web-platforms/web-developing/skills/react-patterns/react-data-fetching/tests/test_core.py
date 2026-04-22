import unittest
from ..core import ReactDataFetching

class TestReactDataFetching(unittest.TestCase):
    def setUp(self):
        self.skill = ReactDataFetching()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
