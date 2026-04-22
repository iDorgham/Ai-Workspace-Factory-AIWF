import unittest
from ..core import CineSeriousDesignLanguage

class TestCineSeriousDesignLanguage(unittest.TestCase):
    def setUp(self):
        self.skill = CineSeriousDesignLanguage()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
