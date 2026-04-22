import unittest
from ..core import LibraryTaxonomyMastery

class TestLibraryTaxonomyMastery(unittest.TestCase):
    def setUp(self):
        self.tax = LibraryTaxonomyMastery()

    def test_audit_taxonomy_integrity_clean(self):
        nodes = [
            {"path": "01-visibility/content/skill-1", "name": "skill-1"},
            {"path": "01-visibility/content/skill-2", "name": "skill-2"}
        ]
        result = self.tax.audit_taxonomy_integrity(nodes)
        self.assertTrue(result["is_taxonomy_integral"])
        self.assertEqual(result["integrity_score"], 100)

    def test_audit_taxonomy_integrity_collision(self):
        nodes = [
            {"path": "path-1", "name": "duplicate"},
            {"path": "path-2", "name": "duplicate"}
        ]
        result = self.tax.audit_taxonomy_integrity(nodes)
        self.assertFalse(result["is_taxonomy_integral"])
        self.assertIn("Naming collision detected", result["violations"][0])

    def test_map_intent_to_skills_match(self):
        intent = "Generate a 3d render of a dubai tower"
        lib_map = {
            "3d-production": ["3d", "render", "mesh"],
            "legal": ["contract", "law"]
        }
        result = self.tax.map_intent_to_skills(intent, lib_map)
        self.assertIn("3d-production", result["mapped_clusters"])
        self.assertEqual(result["recommendation"], "Route to 3d-production engine.")

    def test_map_intent_to_skills_none(self):
        intent = "something unknown"
        result = self.tax.map_intent_to_skills(intent, {})
        self.assertEqual(result["mapped_clusters"], [])
        self.assertEqual(result["recommendation"], "BROAD_RESEARCH_REQUIRED")

    def test_validate_hierarchy_valid(self):
        rels = {"child-1": "parent-1", "child-2": "parent-1"}
        result = self.tax.validate_hierarchy(rels)
        self.assertFalse(result["has_orphans"])
        self.assertEqual(result["hierarchy_status"], "VALIDATED")

    def test_validate_hierarchy_orphans(self):
        rels = {"child-1": None}
        result = self.tax.validate_hierarchy(rels)
        self.assertTrue(result["has_orphans"])
        self.assertEqual(result["hierarchy_status"], "FRAGMENTED")

if __name__ == '__main__':
    unittest.main()
