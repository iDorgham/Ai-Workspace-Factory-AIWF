import unittest
from ..core import EngineeringCoreMastery

class TestEngineeringCoreMastery(unittest.TestCase):
    def setUp(self):
        self.engineering = EngineeringCoreMastery()

    def test_run_architecture_audit(self):
        result = self.engineering.run_architecture_audit(".")
        self.assertIn("status", result)
        self.assertIn("avg_depth", result)

    def test_evaluate_maintainability(self):
        code = '"""Docs"""\ndef test():\n    pass'
        result = self.engineering.evaluate_maintainability(code)
        self.assertGreater(result["doc_ratio"], 0)
        self.assertLessEqual(result["score"], 1.0)

    def test_validate_dependency_mapping(self):
        imports = ["import os", "import os.system", "import subprocess.Popen"]
        violations = self.engineering.validate_dependency_mapping(imports)
        self.assertEqual(len(violations), 2)
        self.assertIn("os.system", violations[0])

if __name__ == '__main__':
    unittest.main()
