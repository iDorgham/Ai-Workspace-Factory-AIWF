import unittest
from ..core import MenaStrategicBrandVoice

class TestMenaStrategicBrandVoice(unittest.TestCase):
    def setUp(self):
        self.skill = MenaStrategicBrandVoice()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
