import unittest
from ..core import VentureDesignMastery

class TestVentureDesignMastery(unittest.TestCase):
    def setUp(self):
        self.skill = VentureDesignMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
