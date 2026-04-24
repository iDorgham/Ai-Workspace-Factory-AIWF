import unittest
from ..core import StructuredLoggingTracing

class TestStructuredLoggingTracing(unittest.TestCase):
    def setUp(self):
        self.skill = StructuredLoggingTracing()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
