import unittest
from ..core import SeoMetadataStrategy

class TestSeoMetadataStrategy(unittest.TestCase):
    def setUp(self):
        self.skill = SeoMetadataStrategy()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
