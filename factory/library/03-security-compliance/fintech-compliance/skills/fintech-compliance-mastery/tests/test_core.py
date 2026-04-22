import unittest
from ..core import FintechComplianceMastery

class TestFintechComplianceMastery(unittest.TestCase):
    def setUp(self):
        self.fin = FintechComplianceMastery()

    def test_audit_payment_security_pass(self):
        config = {"uses_tokenization": True, "stores_cvv": False, "is_pii_encrypted": True}
        result = self.fin.audit_payment_security(config)
        self.assertTrue(result["is_payment_secure"])
        self.assertEqual(result["status"], "PCI_COMPLIANT")

    def test_audit_payment_security_fail_cvv(self):
        config = {"uses_tokenization": True, "stores_cvv": True}
        result = self.fin.audit_payment_security(config)
        self.assertFalse(result["is_payment_secure"])
        self.assertEqual(result["status"], "SECURITY_RISK")

    def test_scan_aml_velocity_critical(self):
        txs = [{"amount": 15000} for _ in range(6)]
        result = self.fin.scan_aml_velocity(txs)
        self.assertTrue(result["risk_flag"])
        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_scan_aml_velocity_low(self):
        txs = [{"amount": 500}]
        result = self.fin.scan_aml_velocity(txs)
        self.assertFalse(result["risk_flag"])

    def test_validate_sandbox_stage_valid(self):
        stats = {"is_sandbox_approved": True, "current_volume_limit": 1000, "current_transaction_volume": 500}
        result = self.fin.validate_sandbox_stage(stats)
        self.assertTrue(result["is_authorized"])
        self.assertEqual(result["status"], "SANDBOX_ACTIVE")

    def test_validate_sandbox_stage_limit_reached(self):
        stats = {"is_sandbox_approved": True, "current_volume_limit": 1000, "current_transaction_volume": 1200}
        result = self.fin.validate_sandbox_stage(stats)
        self.assertFalse(result["is_authorized"])

    def test_calculate_cbe_risk_score_high(self):
        data = {"is_pep": True, "is_high_risk_geo": True}
        result = self.fin.calculate_cbe_risk_score(data)
        self.assertEqual(result["risk_level"], "HIGH")
        self.assertFalse(result["cbe_compliant"])

    def test_audit_e_payment_regulations_compliant(self):
        meta = {"has_mfa_otp": True, "settlement_currency": "EGP", "data_residency_egypt": True}
        result = self.fin.audit_e_payment_regulations(meta)
        self.assertTrue(result["cbe_regulation_compliance"])
        self.assertEqual(result["recommendation"], "OMEGA_CERTIFIED")

if __name__ == '__main__':
    unittest.main()
