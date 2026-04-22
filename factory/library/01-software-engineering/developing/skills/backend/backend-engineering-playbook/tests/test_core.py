import unittest
from ..core import BackendEngineeringPlaybook

class TestBackendEngineeringPlaybook(unittest.TestCase):
    def setUp(self):
        self.skill = BackendEngineeringPlaybook()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
