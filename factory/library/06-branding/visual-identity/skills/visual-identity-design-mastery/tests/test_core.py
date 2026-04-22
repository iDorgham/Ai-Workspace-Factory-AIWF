import unittest
from ..core import VisualIdentityDesignMastery

class TestVisualIdentityDesignMastery(unittest.TestCase):
    def setUp(self):
        self.viz = VisualIdentityDesignMastery()

    def test_audit_negative_space_pass(self):
        logo = {"x_height": 20}
        result = self.viz.audit_negative_space(logo, 25)
        self.assertTrue(result["is_standard"])

    def test_audit_negative_space_fail(self):
        logo = {"x_height": 20}
        result = self.viz.audit_negative_space(logo, 10)
        self.assertFalse(result["is_standard"])

    def test_validate_grid_snap_compliant(self):
        coords = [{"x": 8, "y": 16}, {"x": 24, "y": 40}]
        result = self.viz.validate_grid_snap(coords, 8)
        self.assertTrue(result["is_grid_compliant"])

    def test_validate_grid_snap_violations(self):
        coords = [{"x": 8, "y": 16}, {"x": 23, "y": 40}]
        result = self.viz.validate_grid_snap(coords, 8)
        self.assertFalse(result["is_grid_compliant"])
        self.assertEqual(len(result["violations"]), 1)

    def test_verify_asset_format_vector(self):
        meta = {"extension": "SVG"}
        result = self.viz.verify_asset_format(meta)
        self.assertTrue(result["is_scalable_vector"])

    def test_verify_asset_format_raster(self):
        meta = {"extension": "png"}
        result = self.viz.verify_asset_format(meta)
        self.assertFalse(result["is_scalable_vector"])

if __name__ == '__main__':
    unittest.main()
