import unittest
from ..core import ElectronicCompositionTheory

class TestElectronicCompositionTheory(unittest.TestCase):
    def setUp(self):
        self.skill = ElectronicCompositionTheory()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
