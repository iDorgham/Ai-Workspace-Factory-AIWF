import unittest
from ..core import PresentationalContainerPattern

class TestPresentationalContainerPattern(unittest.TestCase):
    def setUp(self):
        self.skill = PresentationalContainerPattern()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
