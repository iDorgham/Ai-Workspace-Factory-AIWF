import unittest
from ..core import EgyptContractDraftingPhysics

class TestEgyptContractDraftingPhysics(unittest.TestCase):
    def setUp(self):
        self.skill = EgyptContractDraftingPhysics()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
