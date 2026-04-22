import unittest
from ..core import TrainingMastery

class TestTrainingMastery(unittest.TestCase):
    def setUp(self):
        self.skill = TrainingMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
