import unittest
from ..core import ClientSideRendering

class TestClientSideRendering(unittest.TestCase):
    def setUp(self):
        self.skill = ClientSideRendering()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
