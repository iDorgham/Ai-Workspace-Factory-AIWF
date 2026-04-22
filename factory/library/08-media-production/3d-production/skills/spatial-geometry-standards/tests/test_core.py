import unittest
from ..core import SpatialGeometryStandards

class TestSpatialGeometryStandards(unittest.TestCase):
    def setUp(self):
        self.geo = SpatialGeometryStandards()

    def test_audit_topology_clean(self):
        mesh = {"polygon_count": 1000, "tris": 50, "has_ngons": False, "is_manifold": True}
        result = self.geo.audit_topology(mesh)
        self.assertTrue(result["is_topology_clean"])
        self.assertEqual(result["status"], "PRODUCTION_READY")

    def test_audit_topology_messy(self):
        mesh = {"polygon_count": 1000, "tris": 50, "has_ngons": True, "is_manifold": True}
        result = self.geo.audit_topology(mesh)
        self.assertFalse(result["is_topology_clean"])
        self.assertEqual(result["status"], "REQUIRES_REMODELING")

    def test_validate_transforms_valid(self):
        assets = [{"name": "pillar", "scale": [1.0, 1.0, 1.0], "pivot": [0.0, 0.0, 0.0]}]
        result = self.geo.validate_transforms(assets)
        self.assertTrue(result["is_transform_valid"])

    def test_validate_transforms_invalid(self):
        assets = [{"name": "broken_box", "scale": [1.0, 2.0, 1.0], "pivot": [10.0, 0.0, 0.0]}]
        result = self.geo.validate_transforms(assets)
        self.assertFalse(result["is_transform_valid"])
        self.assertEqual(len(result["violations"]), 1)

    def test_simulate_regional_lighting_high_noon(self):
        env = {"latitude": 25.0, "time_hour": 12.0}
        result = self.geo.simulate_regional_lighting(env)
        self.assertEqual(result["lighting_profile"], "DESERT_HIGH_NOON")
        self.assertGreater(result["shadow_sharpness_factor"], 0.9)

if __name__ == '__main__':
    unittest.main()
