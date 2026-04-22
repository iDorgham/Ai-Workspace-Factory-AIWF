import unittest
from ..core import RenderPropsPattern

class TestRenderPropsPattern(unittest.TestCase):
    def setUp(self):
        self.skill = RenderPropsPattern()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
