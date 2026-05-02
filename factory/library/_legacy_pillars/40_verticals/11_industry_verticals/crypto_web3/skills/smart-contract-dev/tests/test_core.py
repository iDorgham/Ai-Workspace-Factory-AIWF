import unittest
from ..core import SmartContractDev

class TestSmartContractDev(unittest.TestCase):
    def setUp(self):
        self.skill = SmartContractDev()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
