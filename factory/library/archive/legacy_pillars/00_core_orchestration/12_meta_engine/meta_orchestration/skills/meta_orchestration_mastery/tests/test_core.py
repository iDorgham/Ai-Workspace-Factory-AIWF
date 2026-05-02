import unittest
import os
from ..core import MetaOrchestrationMastery

class TestMetaOrchestrationMastery(unittest.TestCase):
    def setUp(self):
        self.meta = MetaOrchestrationMastery()

    def test_coordinate_multi_tool_parallel(self):
        complexity = {"dependency_depth": 0, "required_tools_count": 2}
        result = self.meta.coordinate_multi_tool(complexity)
        self.assertEqual(result["execution_strategy"], "PARALLEL")
        self.assertGreater(result["concurrency_limit"], 1)

    def test_coordinate_multi_tool_sequential(self):
        complexity = {"dependency_depth": 3, "required_tools_count": 2}
        result = self.meta.coordinate_multi_tool(complexity)
        self.assertEqual(result["execution_strategy"], "SEQUENTIAL")
        self.assertEqual(result["concurrency_limit"], 1)

    def test_validate_skill_creation_ready(self):
        pattern = {"has_core_logic": True, "has_unit_tests": True, "meets_factory_structure": True}
        result = self.meta.validate_skill_creation(pattern)
        self.assertTrue(result["can_replicate_skill"])
        self.assertEqual(result["status"], "OMEGA_TEMPLATE_READY")

    def test_validate_skill_creation_not_ready(self):
        pattern = {"has_core_logic": True, "has_unit_tests": False, "meets_factory_structure": True}
        result = self.meta.validate_skill_creation(pattern)
        self.assertFalse(result["can_replicate_skill"])

    def test_audit_system_health_aligned(self):
        report = {"active_skills_count": 100, "path_mismatch_count": 0}
        result = self.meta.audit_system_health(report)
        self.assertTrue(result["is_aligned"])
        self.assertEqual(result["health_score"], 100.0)

    def test_audit_system_health_mismatch(self):
        report = {"active_skills_count": 100, "path_mismatch_count": 10}
        result = self.meta.audit_system_health(report)
        self.assertFalse(result["is_aligned"])
        self.assertEqual(result["health_score"], 90.0)

    def test_generate_safety_fork(self):
        target = "factory/library/12-meta-engine/meta-orchestration/skills/meta-orchestration-mastery/core.py"
        result = self.meta.generate_safety_fork(target)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(os.path.exists(f"{target}.bak"))
        # Cleanup
        if os.path.exists(f"{target}.bak"):
            os.remove(f"{target}.bak")

    def test_execute_agent_self_upgrade_mock(self):
        # Create a mock node for self-upgrade
        mock_path = "factory/library/scratch/mock_node"
        os.makedirs(mock_path, exist_ok=True)
        core_file = os.path.join(mock_path, "core.py")
        with open(core_file, 'w') as f: f.write("old logic")
        
        result = self.meta.execute_agent_self_upgrade(mock_path, "new logic")
        self.assertEqual(result["status"], "UPGRADE_COMMITTED_TO_PROD")
        with open(core_file, 'r') as f: self.assertEqual(f.read(), "new logic")
        self.assertTrue(os.path.exists(f"{core_file}.bak"))
        
        # Cleanup
        import shutil
        shutil.rmtree(mock_path)

if __name__ == '__main__':
    unittest.main()
