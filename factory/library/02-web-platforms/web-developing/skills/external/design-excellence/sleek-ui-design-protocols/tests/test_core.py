import unittest
from ..core import SleekUiDesignProtocols

class TestSleekUiDesignProtocols(unittest.TestCase):
    def setUp(self):
        self.design = SleekUiDesignProtocols()

    def test_audit_glassmorphism_pass(self):
        styles = {
            "backdrop-filter": "blur(20px)",
            "background-color": "rgba(255, 255, 255, 0.1)"
        }
        result = self.design.audit_glassmorphism(styles)
        self.assertTrue(result["is_glassmorphism_standard"])
        self.assertLessEqual(result["opacity_alpha"], 0.3)

    def test_audit_glassmorphism_fail(self):
        styles = {
            "backdrop-filter": "none",
            "background-color": "rgba(255, 255, 255, 1.0)"
        }
        result = self.design.audit_glassmorphism(styles)
        self.assertFalse(result["is_glassmorphism_standard"])

    def test_audit_typographic_hierarchy_header(self):
        config = {"font-weight": 800, "is_header": True}
        result = self.design.audit_typographic_hierarchy(config)
        self.assertTrue(result["is_authoritative"])

    def test_generate_layered_shadow(self):
        shadow = self.design.generate_layered_shadow(layers=2)
        self.assertIn("0 2px 4px", shadow)
        self.assertIn("0 4px 8px", shadow)

if __name__ == '__main__':
    unittest.main()
