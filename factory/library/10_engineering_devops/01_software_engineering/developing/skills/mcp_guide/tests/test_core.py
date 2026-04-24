import unittest
from ..core import McpGuide

class TestMcpGuide(unittest.TestCase):
    def setUp(self):
        self.skill = McpGuide()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
