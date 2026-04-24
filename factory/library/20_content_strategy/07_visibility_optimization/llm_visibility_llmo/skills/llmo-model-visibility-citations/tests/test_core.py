import unittest
from ..core import LlmoModelVisibilityCitations

class TestLlmoModelVisibilityCitations(unittest.TestCase):
    def setUp(self):
        self.skill = LlmoModelVisibilityCitations()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
