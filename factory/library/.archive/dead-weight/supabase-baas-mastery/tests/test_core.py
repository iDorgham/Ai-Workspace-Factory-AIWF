import unittest
from ..core import SupabaseBaasMastery

class TestSupabaseBaasMastery(unittest.TestCase):
    def setUp(self):
        self.skill = SupabaseBaasMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
