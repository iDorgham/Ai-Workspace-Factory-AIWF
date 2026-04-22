import unittest
from ..core import DynamicMemoryProtocol

class TestDynamicMemoryProtocol(unittest.TestCase):
    def setUp(self):
        self.skill = DynamicMemoryProtocol()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
