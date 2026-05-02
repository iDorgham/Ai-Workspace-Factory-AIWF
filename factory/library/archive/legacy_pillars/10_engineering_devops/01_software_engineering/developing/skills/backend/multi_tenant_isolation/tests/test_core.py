import unittest
from ..core import MultiTenantIsolation

class TestMultiTenantIsolation(unittest.TestCase):
    def setUp(self):
        self.skill = MultiTenantIsolation()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
