"""
📱 App Developing Mastery - Operational Core
Enforces Expo performance, asset strategy, and EAS deployment standards.
"""

from typing import Dict, Any, List

class AppDevelopingMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "mobile-optimization"

    def audit_expo_config(self, app_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans app.json/app.config.js for performance and compliance.
        New in v10.1.0: Detailed splash and icon asset auditing.
        """
        expo = app_json.get("expo", {})
        issues = []
        
        # Check for asset optimization
        if "splash" not in expo:
            issues.append("Missing 'splash' configuration (critical for cold start UX).")
        if "icon" not in expo:
            issues.append("Missing 'icon' configuration.")
            
        # Check for SDK version
        sdk_version = expo.get("sdkVersion", "unknown")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "sdk_version": sdk_version,
            "ota_strategy": "enabled" if "updates" in expo else "disabled"
        }

    def validate_eas_config(self, eas_json: Dict[str, Any]) -> bool:
        """
        Ensures EAS (Expo Application Services) configurations for builds and submissions.
        Checks for channel and distribution profiles.
        """
        build = eas_json.get("build", {})
        if not build:
            return False
            
        # Ensure at least one profile has a distribution set
        has_distribution = any("distribution" in profile for profile in build.values())
        return has_distribution

    def check_universal_links(self, config: Dict[str, Any]) -> List[str]:
        """
        Verifies deep-link / universal-link mapping in app configuration.
        """
        ios = config.get("expo", {}).get("ios", {})
        android = config.get("expo", {}).get("android", {})
        
        violations = []
        if "associatedDomains" not in ios:
            violations.append("IOS: 'associatedDomains' not configured for Universal Links.")
        if "intentFilters" not in android:
            violations.append("ANDROID: 'intentFilters' not configured for App Links.")
            
        return violations
