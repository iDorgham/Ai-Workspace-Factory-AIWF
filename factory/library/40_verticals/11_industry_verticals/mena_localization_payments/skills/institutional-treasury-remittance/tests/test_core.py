import unittest
from core import InstitutionalTreasuryRemittance

class TestInstitutionalTreasuryRemittance(unittest.TestCase):
    def setUp(self):
        self.bank = InstitutionalTreasuryRemittance()

    def test_calculate_treasury_balance(self):
        txs = [
            {"currency": "EGP", "amount": 1000000},
            {"currency": "AED", "amount": 50000}
        ]
        result = self.bank.calculate_treasury_balance(txs)
        self.assertEqual(result["balances"]["EGP"], 1000000)
        self.assertEqual(result["balances"]["AED"], 50000)

    def test_authorize_escrow_settlement_passing_egypt(self):
        data = {
            "id": "SETTLE_001",
            "region": "EGY",
            "amount": 500000,
            "escrow_account_verified": True,
            "development_stage_certified": True
        }
        result = self.bank.authorize_escrow_settlement(data)
        self.assertEqual(result["status"], "AUTHORIZED_ESCROW")
        self.assertTrue(result["compliance_flags"]["egypt_off_plan_law_pass"])

    def test_authorize_escrow_settlement_failing_egypt(self):
        data = {
            "id": "SETTLE_002",
            "region": "EGY",
            "amount": 500000,
            "escrow_account_verified": False, # Illegal for off-plan
            "development_stage_certified": True
        }
        result = self.bank.authorize_escrow_settlement(data)
        self.assertEqual(result["status"], "COMPLIANCE_HOLD_ESCROW_REQUIRED")
        self.assertFalse(result["compliance_flags"]["egypt_off_plan_law_pass"])

    def test_validate_iban_format(self):
        self.assertTrue(self.bank.validate_iban_format("AE1234567890123456"))
        self.assertFalse(self.bank.validate_iban_format("123"))

if __name__ == '__main__':
    unittest.main()
