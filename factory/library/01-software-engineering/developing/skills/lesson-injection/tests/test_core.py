import unittest
from ..core import LessonInjection

class TestLessonInjection(unittest.TestCase):
    def setUp(self):
        self.skill = LessonInjection()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
