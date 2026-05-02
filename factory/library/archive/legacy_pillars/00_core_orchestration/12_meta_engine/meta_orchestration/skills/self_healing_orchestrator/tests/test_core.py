import unittest
import os
from pathlib import Path
from ..core import SelfHealingOrchestrator

class TestSelfHealingOrchestrator(unittest.TestCase):
    def setUp(self):
        self.healer = SelfHealingOrchestrator()
        self.temp_file = Path("factory/library/scratch/mock_missing.py")

    def test_detect_structural_violations(self):
        report = {
            "violations": [
                {"violation_type": "missing_stub", "target_path": "path/a.py"},
                {"violation_type": "performance_low", "target_path": "path/b.py"}
            ]
        }
        violations = self.healer.detect_structural_violations(report)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["violation_type"], "missing_stub")

    def test_apply_structural_patch_healing(self):
        violation = {"violation_type": "missing_stub", "target_path": str(self.temp_file)}
        result = self.healer.apply_structural_patch(violation)
        self.assertEqual(result["status"], "HEALED")
        self.assertTrue(self.temp_file.exists())
        # Cleanup
        if self.temp_file.exists():
            self.temp_file.unlink()

if __name__ == '__main__':
    unittest.main()
