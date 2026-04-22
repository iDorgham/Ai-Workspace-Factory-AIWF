"""
⚡ Sentry Official Mastery - Operational Core
Enforces standards for full-stack observability, error grouping, and tracing thresholds.
"""

from typing import Dict, Any, List

class SentryOfficialMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "observability-engineering"

    def audit_error_fingerprinting(self, error_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits error grouping/fingerprinting strategy.
        Rule: Use custom fingerprinting for recurring but varied errors (e.g., database connection peaks).
        """
        fingerprint = error_report.get("fingerprint", [])
        error_type = error_report.get("type", "Unknown")
        
        # Generic fingerprinting is the default (empty list or just type)
        is_generic = len(fingerprint) <= 1
        
        return {
            "has_custom_fingerprint": not is_generic,
            "fingerprint": fingerprint,
            "is_optimized": not is_generic if "Database" in error_type else True,
            "recommendation": "Implement custom fingerprinting for this recurring high-volume error type." if is_generic and "Database" in error_type else "OBSERVABILITY_TUNED"
        }

    def validate_tracing_thresholds(self, performance_stats: Dict[str, float]) -> Dict[str, Any]:
        """
        Validates Performance Tracing (LCP/FID) thresholds.
        Target: LCP < 2.5s, FID < 100ms.
        """
        lcp = performance_stats.get("lcp", 0.0)
        fid = performance_stats.get("fid", 0.0)
        
        lcp_compliant = lcp < 2500.0
        fid_compliant = fid < 100.0
        
        return {
            "is_tracing_compliant": lcp_compliant and fid_compliant,
            "lcp_ms": lcp,
            "fid_ms": fid,
            "status": "HEALTHY" if lcp_compliant and fid_compliant else "DEGRADED"
        }

    def verify_tag_depth(self, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        Ensures telemetry tags provide enough context for root-cause analysis (RCA).
        Mandatory Tags: environment, release, server_name, user_id (if available).
        """
        mandatory = ["environment", "release", "server_name"]
        missing = [tag for tag in mandatory if tag not in tags]
        
        return {
            "is_context_rich": len(missing) == 0,
            "missing_tags": missing,
            "tags_count": len(tags)
        }
