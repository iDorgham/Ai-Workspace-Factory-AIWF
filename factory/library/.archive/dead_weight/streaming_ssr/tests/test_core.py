import unittest
from ..core import StreamingSsr

class TestStreamingSsr(unittest.TestCase):
    def setUp(self):
        self.skill = StreamingSsr()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
