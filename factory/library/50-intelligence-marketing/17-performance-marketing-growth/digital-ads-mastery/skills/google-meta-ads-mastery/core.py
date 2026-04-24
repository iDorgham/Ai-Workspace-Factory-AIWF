"""
📊 Google & Meta Ads Mastery - Operational Core
Algorithmic budget scaling, ROAS auditing, and Conversions API (CAPI) health scanning.
"""

from typing import Dict, Any, List

class GoogleMetaAdsMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "marketing-automation"

    def audit_roas_scaling(self, ad_set_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates ad set performance and provides a scaling recommendation.
        Rule: If ROAS > 3.0, increase budget by 20% every 48h.
        """
        roas = ad_set_performance.get("roas", 0.0)
        current_daily_budget = ad_set_performance.get("daily_budget", 0.0)
        hours_since_last_change = ad_set_performance.get("hours_since_change", 0)
        
        recommendation = "HOLD"
        new_budget = current_daily_budget
        
        if roas > 3.0:
            if hours_since_last_change >= 48:
                recommendation = "SCALE_UP"
                new_budget = current_daily_budget * 1.2
            else:
                recommendation = "WAIT_FOR_STABILITY"
        elif roas < 1.5:
            recommendation = "SCALE_DOWN"
            new_budget = current_daily_budget * 0.8
            
        return {
            "roas": roas,
            "recommendation": recommendation,
            "new_recommended_budget": round(new_budget, 2),
            "logic": "20percent-progressive-scaling"
        }

    def verify_tracking_health(self, tracking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans for Pixel and CAPI (Conversions API) active states.
        """
        pixel_active = tracking_data.get("pixel_status") == "active"
        capi_active = tracking_data.get("capi_status") == "active"
        
        is_healthy = pixel_active and capi_active
        
        warnings = []
        if not pixel_active: warnings.append("Pixel is INACTIVE or missing.")
        if not capi_active: warnings.append("Converson API (CAPI) is INACTIVE or missing.")
        
        return {
            "is_tracking_healthy": is_healthy,
            "warnings": warnings,
            "status": "GREEN" if is_healthy else "RED"
        }

    def calculate_creative_refresh_urgency(self, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates urgency to refresh creative based on 'Ad Fatigue' signals (CTR drop).
        """
        days_active = ad_data.get("days_active", 0)
        ctr_trend = ad_data.get("ctr_trend", 0) # e.g., -0.2 for 20% drop
        
        urgency = "LOW"
        if days_active > 14 or ctr_trend < -0.15:
            urgency = "HIGH"
        elif days_active > 10 or ctr_trend < -0.1:
            urgency = "MEDIUM"
            
        return {
            "days_active": days_active,
            "ctr_trend_signal": ctr_trend,
            "refresh_urgency": urgency,
            "reason": "Fatigue detected" if ctr_trend < -0.15 else "Duration threshold met" if days_active > 14 else "Healthy"
        }
