import unittest
from ..core import WebglPhaserThreejsMastery

class TestWebglPhaserThreejsMastery(unittest.TestCase):
    def setUp(self):
        self.skill = WebglPhaserThreejsMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
