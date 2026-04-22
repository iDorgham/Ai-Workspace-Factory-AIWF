import unittest
from ..core import CloudArchitectureMastery

class TestCloudArchitectureMastery(unittest.TestCase):
    def setUp(self):
        self.skill = CloudArchitectureMastery()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
