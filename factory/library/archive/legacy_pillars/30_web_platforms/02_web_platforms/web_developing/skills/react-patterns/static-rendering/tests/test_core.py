import unittest
from ..core import StaticRendering

class TestStaticRendering(unittest.TestCase):
    def setUp(self):
        self.skill = StaticRendering()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
