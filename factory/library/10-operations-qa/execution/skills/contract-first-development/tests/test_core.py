import unittest
from ..core import ContractFirstDevelopment

class TestContractFirstDevelopment(unittest.TestCase):
    def setUp(self):
        self.skill = ContractFirstDevelopment()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
