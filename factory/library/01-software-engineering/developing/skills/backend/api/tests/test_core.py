import unittest
from ..core import Api

class TestApi(unittest.TestCase):
    def setUp(self):
        self.skill = Api()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
