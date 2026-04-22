import unittest
from ..core import WorkspaceAuditOrchestrator

class TestWorkspaceAuditOrchestrator(unittest.TestCase):
    def setUp(self):
        self.skill = WorkspaceAuditOrchestrator()

    def test_validate_config(self):
        self.assertTrue(self.skill.validate_config({}))

if __name__ == '__main__':
    unittest.main()
