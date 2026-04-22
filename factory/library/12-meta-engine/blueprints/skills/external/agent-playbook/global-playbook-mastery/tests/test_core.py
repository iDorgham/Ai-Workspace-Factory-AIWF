import unittest
from ..core import GlobalPlaybookMastery

class TestGlobalPlaybookMastery(unittest.TestCase):
    def setUp(self):
        self.skill = GlobalPlaybookMastery()

    def test_run_operational_logic(self):
        self.assertTrue(self.skill.run_operational_logic({}))

if __name__ == '__main__':
    unittest.main()
