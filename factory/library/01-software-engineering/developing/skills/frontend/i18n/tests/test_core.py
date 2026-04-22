import unittest
from ..core import I18N

class TestI18N(unittest.TestCase):
    def setUp(self):
        self.skill = I18N()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
