"""
☁️ Azure Cloud Physics - Operational Core
Enforces enterprise standards for RBAC Security, High Availability, and Cost Management.
"""

from typing import Dict, Any, List

class AzureCloudPhysics:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "enterprise-cloud-architecture"

    def audit_rbac_security(self, infrastructure_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits infrastructure for Managed Identity usage vs. hardcoded secrets.
        Rule: Use System-Assigned or User-Assigned Managed Identities for resource access.
        """
        has_managed_identity = infrastructure_config.get("managed_identity_enabled", False)
        has_secrets = infrastructure_config.get("hardcoded_secrets_detected", False)
        
        is_secure = has_managed_identity and not has_secrets
        
        return {
            "is_rbac_compliant": is_secure,
            "managed_identity_active": has_managed_identity,
            "secrets_risk_detected": has_secrets,
            "recommendation": "Transition to Managed Identities and Azure Key Vault for all resource credentials." if not is_secure else "ENTERPRISE_SECURE"
        }

    def audit_high_availability(self, deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies Availability Zone (AZ) distribution for HA compliance.
        Rule: Critical assets must be distributed across 3 zones within a region.
        """
        zones = deployment_config.get("availability_zones", [])
        is_global_lb = deployment_config.get("has_global_load_balancer", False) # e.g., Azure Front Door
        
        is_ha_compliant = len(zones) >= 3 and is_global_lb
        
        return {
            "is_ha_compliant": is_ha_compliant,
            "zone_count": len(zones),
            "load_balancer": "GLOBAL" if is_global_lb else "LOCAL/NONE",
            "redundancy_level": "OPTIMAL" if is_ha_compliant else "PARTIAL"
        }

    def validate_budget_alerts(self, cost_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates cost-alert thresholds.
        Rule: Alerts must be set at 50%, 75%, and 90% of monthly budget.
        """
        alerts = cost_config.get("alert_thresholds", [])
        mandatory = [50, 75, 90]
        
        missing = [m for m in mandatory if m not in alerts]
        
        return {
            "is_budget_monitored": len(missing) == 0,
            "current_alerts": alerts,
            "missing_thresholds": missing,
            "status": "CONTROLLED" if not missing else "FINANCIAL_RISK"
        }
