import unittest
from ..core import ThreeDProductionMastery

class TestThreeDProductionMastery(unittest.TestCase):
    def setUp(self):
        self.three = ThreeDProductionMastery()

    def test_audit_mesh_density_pass(self):
        meta = {"poly_count": 45000}
        result = self.three.audit_mesh_density(meta)
        self.assertTrue(result["is_compliant"])
        self.assertEqual(result["status"], "WEB_GL_READY")

    def test_audit_mesh_density_fail(self):
        meta = {"poly_count": 120000}
        result = self.three.audit_mesh_density(meta)
        self.assertFalse(result["is_compliant"])
        self.assertGreater(result["reduction_required_pct"], 50)

    def test_verify_texture_atlas_optimized(self):
        stats = {"draw_calls": 2, "is_atlased": False}
        result = self.three.verify_texture_atlas(stats)
        self.assertTrue(result["is_optimized"])

    def test_verify_texture_atlas_not_optimized(self):
        stats = {"draw_calls": 15, "is_atlased": False}
        result = self.three.verify_texture_atlas(stats)
        self.assertFalse(result["is_optimized"])

    def test_check_pbr_integrity_omega(self):
        meta = {"has_normal_map": True, "has_roughness_map": True, "has_metallic_map": True}
        result = self.three.check_pbr_integrity(meta)
        self.assertTrue(result["is_high_fidelity"])
        self.assertEqual(result["fidelity_tier"], "OMEGA")

if __name__ == '__main__':
    unittest.main()
