import unittest
from ..core import EntityKnowledgeGraphManagement

class TestEntityKnowledgeGraphManagement(unittest.TestCase):
    def setUp(self):
        self.skill = EntityKnowledgeGraphManagement()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
