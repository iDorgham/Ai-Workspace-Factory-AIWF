import unittest
from ..core import SbomSecretManagement

class TestSbomSecretManagement(unittest.TestCase):
    def setUp(self):
        self.skill = SbomSecretManagement()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
