import unittest
from ..core import PlatformAgnosticContracts

class TestPlatformAgnosticContracts(unittest.TestCase):
    def setUp(self):
        self.skill = PlatformAgnosticContracts()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
