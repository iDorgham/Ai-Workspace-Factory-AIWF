import unittest
from ..core import ArabicTypographyRtlPhysics

class TestArabicTypographyRtlPhysics(unittest.TestCase):
    def setUp(self):
        self.rtl = ArabicTypographyRtlPhysics()

    def test_calculate_optical_balance(self):
        # 16pt English should recommend 17.5pt Arabic
        result = self.rtl.calculate_optical_balance(16.0)
        self.assertEqual(result["recommended_arabic_size"], 17.5)
        self.assertTrue(result["is_standard"])

    def test_optimize_leading_arabic(self):
        # Base 16pt, +25% leading for Arabic
        # 16 * (1.4 * 1.25) = 16 * 1.75 = 28
        leading = self.rtl.optimize_leading(16.0, is_arabic=True)
        self.assertEqual(leading, 28.0)

    def test_optimize_leading_english(self):
        # Base 16pt, standard 1.4 for English
        # 16 * 1.4 = 22.4
        leading = self.rtl.optimize_leading(16.0, is_arabic=False)
        self.assertEqual(leading, 22.4)

    def test_audit_rtl_mirroring_violations(self):
        elements = [
            {"name": "BodyText", "alignment": "left"},
            {"name": "BackButton", "type": "icon-back", "faces": "left", "alignment": "right"}
        ]
        result = self.rtl.audit_rtl_mirroring(elements)
        self.assertFalse(result["is_rtl_compliant"])
        self.assertEqual(len(result["violations"]), 2)

    def test_audit_rtl_mirroring_pass(self):
        elements = [
            {"name": "BodyText", "alignment": "right"},
            {"name": "BackButton", "type": "icon-back", "faces": "right", "alignment": "right"}
        ]
        result = self.rtl.audit_rtl_mirroring(elements)
        self.assertTrue(result["is_rtl_compliant"])

if __name__ == '__main__':
    unittest.main()
