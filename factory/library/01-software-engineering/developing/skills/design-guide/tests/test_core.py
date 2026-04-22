import unittest
from ..core import DesignGuide

class TestDesignGuide(unittest.TestCase):
    def setUp(self):
        self.skill = DesignGuide()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
