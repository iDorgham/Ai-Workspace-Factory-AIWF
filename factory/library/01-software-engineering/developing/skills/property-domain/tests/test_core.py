import unittest
from ..core import PropertyDomain

class TestPropertyDomain(unittest.TestCase):
    def setUp(self):
        self.skill = PropertyDomain()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
