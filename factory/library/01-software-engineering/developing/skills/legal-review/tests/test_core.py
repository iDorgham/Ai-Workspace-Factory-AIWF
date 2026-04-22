import unittest
from ..core import LegalReview

class TestLegalReview(unittest.TestCase):
    def setUp(self):
        self.skill = LegalReview()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
