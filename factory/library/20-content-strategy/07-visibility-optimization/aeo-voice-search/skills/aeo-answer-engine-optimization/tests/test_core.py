import unittest
from ..core import AeoAnswerEngineOptimization

class TestAeoAnswerEngineOptimization(unittest.TestCase):
    def setUp(self):
        self.skill = AeoAnswerEngineOptimization()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
