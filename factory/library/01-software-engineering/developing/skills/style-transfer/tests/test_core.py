import unittest
from ..core import StyleTransfer

class TestStyleTransfer(unittest.TestCase):
    def setUp(self):
        self.skill = StyleTransfer()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
