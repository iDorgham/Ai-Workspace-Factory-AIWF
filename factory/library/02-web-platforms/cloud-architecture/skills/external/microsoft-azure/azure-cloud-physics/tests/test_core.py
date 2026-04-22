import unittest
from ..core import AzureCloudPhysics

class TestAzureCloudPhysics(unittest.TestCase):
    def setUp(self):
        self.cloud = AzureCloudPhysics()

    def test_audit_rbac_security_pass(self):
        config = {"managed_identity_enabled": True, "hardcoded_secrets_detected": False}
        result = self.cloud.audit_rbac_security(config)
        self.assertTrue(result["is_rbac_compliant"])

    def test_audit_rbac_security_fail_secrets(self):
        config = {"managed_identity_enabled": True, "hardcoded_secrets_detected": True}
        result = self.cloud.audit_rbac_security(config)
        self.assertFalse(result["is_rbac_compliant"])

    def test_audit_high_availability_full(self):
        config = {"availability_zones": [1, 2, 3], "has_global_load_balancer": True}
        result = self.cloud.audit_high_availability(config)
        self.assertTrue(result["is_ha_compliant"])
        self.assertEqual(result["redundancy_level"], "OPTIMAL")

    def test_audit_high_availability_partial(self):
        config = {"availability_zones": [1, 2], "has_global_load_balancer": True}
        result = self.cloud.audit_high_availability(config)
        self.assertFalse(result["is_ha_compliant"])

    def test_validate_budget_alerts_complete(self):
        config = {"alert_thresholds": [50, 75, 90]}
        result = self.cloud.validate_budget_alerts(config)
        self.assertTrue(result["is_budget_monitored"])

    def test_validate_budget_alerts_missing(self):
        config = {"alert_thresholds": [50]}
        result = self.cloud.validate_budget_alerts(config)
        self.assertFalse(result["is_budget_monitored"])
        self.assertEqual(len(result["missing_thresholds"]), 2)

if __name__ == '__main__':
    unittest.main()
