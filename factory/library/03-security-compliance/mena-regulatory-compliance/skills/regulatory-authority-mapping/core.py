"""
🏛️ Regulatory Authority Mapping - Operational Core
Enforces MENA regional jurisdictional routing, license-gate validation, and data sovereignty rules.
"""

from typing import Dict, Any, List

class RegulatoryAuthorityMapping:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "jurisdictional-compliance-routing"

    def route_to_regulator(self, business_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes the business model to the correct regulatory node in UAE/Egypt.
        Factors: Activity Type (Crypto, Banking, Mainland), Region (Dubai, Abu Dhabi, Egypt).
        """
        region = business_model.get("region", "Mainland Dubai").lower()
        activity = business_model.get("activity", "Generic").lower()
        
        # Logic for UAE Jurisdictions
        if "dubai" in region:
            if any(x in activity for x in ["crypto", "web3", "virtual asset"]):
                if "difc" in region:
                    return {"authority": "DFSA", "jurisdiction": "DIFC", "framework": "DIFC Financial Law"}
                return {"authority": "VARA", "jurisdiction": "Dubai (Non-DIFC)", "framework": "VARA Regulations"}
            
            if any(x in activity for x in ["banking", "payment", "insurance"]):
                if "difc" in region:
                    return {"authority": "DFSA", "jurisdiction": "DIFC", "framework": "DIFC Financial Law"}
                return {"authority": "CBUAE", "jurisdiction": "Mainland/Onshore", "framework": "Federal Banking Law"}
            
            return {"authority": "DED", "jurisdiction": "Mainland", "framework": "Commercial Companies Law"}

        if "abu dhabi" in region:
            if "adgm" in region:
                return {"authority": "FSRA", "jurisdiction": "ADGM", "framework": "Common Law"}
            return {"authority": "CBUAE / AD-DED", "jurisdiction": "Mainland", "framework": "Federal Law"}

        # Logic for Egypt Jurisdictions
        if "egypt" in region:
            if any(x in activity for x in ["banking", "pay", "digital wallet"]):
                return {"authority": "CBE", "jurisdiction": "National", "framework": "Law No. 194 of 2020"}
            if any(x in activity for x in ["micro-finance", "insurance", "capital"]):
                return {"authority": "FRA", "jurisdiction": "National", "framework": "Law No. 10 of 2009"}
            return {"authority": "GAFI / ITIDA", "jurisdiction": "National", "framework": "Investment Law No. 72"}

        return {"authority": "UNKNOWN", "jurisdiction": region, "framework": "REQUIRES_LEGAL_AUDIT"}

    def audit_data_sovereignty(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates regional data-residency rules (Data Localization).
        Rule: Financial/Health data must stay in-region unless explicitly exempted.
        """
        data_type = architecture.get("data_type", "Generic").lower()
        storage_region = architecture.get("storage_region", "Global").lower()
        company_region = architecture.get("company_region", "UAE").lower()
        
        needs_localization = any(x in data_type for x in ["financial", "health", "biometric", "government"])
        is_localized = company_region in storage_region
        
        status = "COMPLIANT" if not needs_localization or is_localized else "DATA_SOVEREIGNTY_RISK"
        
        return {
            "status": status,
            "needs_localization": needs_localization,
            "storage_match": is_localized,
            "recommendation": f"Migrate {data_type} storage to {company_region} local data centers." if status == "DATA_SOVEREIGNTY_RISK" else "CONTINUE"
        }

    def validate_anti_patterns(self, application_path: Dict[str, str]) -> Dict[str, Any]:
        """
        Flags common mis-routing errors for MENA regulators.
        Example: Applying to DED for Crypto licensing.
        """
        authority = application_path.get("selected_authority", "").upper()
        activity = application_path.get("activity", "").lower()
        
        is_invalid = (authority == "DED" and any(x in activity for x in ["crypto", "web3", "virtual asset"]))
        
        return {
            "is_path_valid": not is_invalid,
            "blocker_reason": "VARA (Dubai) or ADGM (Abu Dhabi) is required for Virtual Asset activities." if is_invalid else "NONE"
        }
