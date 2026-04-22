import unittest
from ..core import BusinessIncorporationUae

class TestBusinessIncorporationUae(unittest.TestCase):
    def setUp(self):
        self.skill = BusinessIncorporationUae()

    def test_validate_metrics(self):
        self.assertTrue(self.skill.validate_metrics({}))

if __name__ == '__main__':
    unittest.main()
