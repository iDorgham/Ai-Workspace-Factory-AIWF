import unittest
from ..core import ProgrammaticAdsMastery

class TestProgrammaticAdsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = ProgrammaticAdsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
