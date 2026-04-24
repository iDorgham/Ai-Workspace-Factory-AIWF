import unittest
from ..core import SpecToImplementationMastery

class TestSpecToImplementationMastery(unittest.TestCase):
    def setUp(self):
        self.skill = SpecToImplementationMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
