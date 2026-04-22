import unittest
from ..core import FirebaseIntegration

class TestFirebaseIntegration(unittest.TestCase):
    def setUp(self):
        self.skill = FirebaseIntegration()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
