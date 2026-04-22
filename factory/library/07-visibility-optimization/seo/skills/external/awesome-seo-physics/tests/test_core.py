import unittest
from ..core import AwesomeSeoPhysics

class TestAwesomeSeoPhysics(unittest.TestCase):
    def setUp(self):
        self.skill = AwesomeSeoPhysics()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
