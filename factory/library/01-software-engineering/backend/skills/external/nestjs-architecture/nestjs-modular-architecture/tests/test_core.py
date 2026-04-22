import unittest
from ..core import NestjsModularArchitecture

class TestNestjsModularArchitecture(unittest.TestCase):
    def setUp(self):
        self.skill = NestjsModularArchitecture()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
