import unittest
from ..core import CompoundEngineering

class TestCompoundEngineering(unittest.TestCase):
    def setUp(self):
        self.skill = CompoundEngineering()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
