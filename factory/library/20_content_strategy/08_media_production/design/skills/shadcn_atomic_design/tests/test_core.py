import unittest
from ..core import ShadcnAtomicDesign

class TestShadcnAtomicDesign(unittest.TestCase):
    def setUp(self):
        self.skill = ShadcnAtomicDesign()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
