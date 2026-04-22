import unittest
from ..core import HealthTechPharmaMastery

class TestHealthTechPharmaMastery(unittest.TestCase):
    def setUp(self):
        self.health = HealthTechPharmaMastery()

    def test_anonymize_patient_data(self):
        records = [
            {"patient_name": "Dorgham", "dob": "1990-05-20", "phone": "+20123456789", "diagnosis": "Stable"}
        ]
        result = self.health.anonymize_patient_data(records)
        self.assertEqual(result[0]["patient_name"], "REDACTED")
        self.assertEqual(result[0]["dob"], "1990-01-01")
        self.assertEqual(result[0]["phone"], "XXXX-XXXX")
        self.assertEqual(result[0]["diagnosis"], "Stable") # Medical data remains

    def test_audit_regulatory_gap_compliant(self):
        manifest = {
            "data_encryption_at_rest": True,
            "audit_logging_active": True,
            "local_data_residency_confirmed": True
        }
        result = self.health.audit_regulatory_gap(manifest)
        self.assertTrue(result["is_compliant"])
        self.assertEqual(result["tier"], "💎 OMEGA")

    def test_audit_regulatory_gap_fail(self):
        manifest = {
            "data_encryption_at_rest": True,
            "local_data_residency_confirmed": False
        }
        result = self.health.audit_regulatory_gap(manifest)
        self.assertFalse(result["is_compliant"])
        self.assertIn("audit_logging_active", result["detected_gaps"])
        self.assertEqual(result["residency_status"], "EXTERNAL_EXPOSURE")

if __name__ == '__main__':
    unittest.main()
