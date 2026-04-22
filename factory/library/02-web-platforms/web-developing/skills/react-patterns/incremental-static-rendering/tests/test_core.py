import unittest
from ..core import IncrementalStaticRendering

class TestIncrementalStaticRendering(unittest.TestCase):
    def setUp(self):
        self.skill = IncrementalStaticRendering()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
