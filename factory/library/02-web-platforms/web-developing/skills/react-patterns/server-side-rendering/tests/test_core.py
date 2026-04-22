import unittest
from ..core import ServerSideRendering

class TestServerSideRendering(unittest.TestCase):
    def setUp(self):
        self.skill = ServerSideRendering()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
