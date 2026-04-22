import unittest
from ..core import PaymentCompliance

class TestPaymentCompliance(unittest.TestCase):
    def setUp(self):
        self.pay = PaymentCompliance()

    def test_audit_pci_scope_pass(self):
        flow = {"uses_hosted_fields": True, "uses_tokenization": True, "server_touches_pan": False}
        result = self.pay.audit_pci_scope(flow)
        self.assertTrue(result["is_pci_saq_a_compliant"])
        self.assertEqual(result["risk_level"], "LOW")

    def test_audit_pci_scope_fail(self):
        flow = {"uses_hosted_fields": True, "server_touches_pan": True}
        result = self.pay.audit_pci_scope(flow)
        self.assertFalse(result["is_pci_saq_a_compliant"])
        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_validate_kyc_tier_low(self):
        customer = {"kyc_tier": 1}
        result = self.pay.validate_kyc_tier(customer, 1000, "AED")
        self.assertTrue(result["is_compliant"])
        self.assertEqual(result["required_tier"], 1)

    def test_validate_kyc_tier_high_need_edd(self):
        customer = {"kyc_tier": 1}
        result = self.pay.validate_kyc_tier(customer, 50000, "AED")
        self.assertFalse(result["is_compliant"])
        self.assertEqual(result["required_tier"], 3)

    def test_check_regional_gateways_egypt(self):
        gateways = self.pay.check_regional_gateways("EG")
        self.assertIn("Fawry", gateways)
        self.assertIn("PayMob", gateways)

    def test_generate_idempotency_key(self):
        key = self.pay.generate_idempotency_key("order_123")
        self.assertTrue(key.startswith("pay_order_123_"))

if __name__ == '__main__':
    unittest.main()
