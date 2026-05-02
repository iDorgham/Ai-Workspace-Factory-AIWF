import unittest
from ..core import AntigravityAwesomeMastery

class TestAntigravityAwesomeMastery(unittest.TestCase):
    def setUp(self):
        self.skill = AntigravityAwesomeMastery()

    def test_run_operational_logic(self):
        self.assertTrue(self.skill.run_operational_logic({}))

if __name__ == '__main__':
    unittest.main()
