import unittest
from ..core import SupabaseIntegration

class TestSupabaseIntegration(unittest.TestCase):
    def setUp(self):
        self.skill = SupabaseIntegration()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
