import unittest
from ..core import ReactServerComponents

class TestReactServerComponents(unittest.TestCase):
    def setUp(self):
        self.skill = ReactServerComponents()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
