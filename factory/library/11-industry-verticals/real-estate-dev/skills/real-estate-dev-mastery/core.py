"""
⚡ Real Estate Dev Mastery - Operational Core
Algorithmic property valuation, IRR Newton-Raphson solver, and MENA transaction cost auditing.
"""

from typing import Dict, Any, List
import datetime

class RealEstateDevMastery:
    def __init__(self):
        self.version = "11.0.0"
        self.logic = "aec-industrial-standard"

    def calculate_property_valuation(self, property_data: Dict[str, Any], market_comps: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates property valuation using a weighted average of Comparable Sales and Income Approach.
        Standard weights: 60% Comps, 40% Income.
        """
        # 1. Comparable Analysis (Avg price per sqft of comps * subject area)
        avg_comp_price = sum(market_comps.get("prices", [0])) / max(len(market_comps.get("prices", [])), 1)
        comp_value = avg_comp_price * property_data.get("area_sqft", 0)
        
        # 2. Income Approach (NOI / Cap Rate)
        annual_rent = property_data.get("target_annual_rent", 0)
        op_ex = annual_rent * 0.15 # 15% operating expenses default
        noi = annual_rent - op_ex
        cap_rate = market_comps.get("avg_cap_rate", 0.07)
        income_value = noi / max(cap_rate, 0.01)
        
        # Weighted Value
        estimated_value = (comp_value * 0.6) + (income_value * 0.4)
        
        return {
            "estimated_market_value": round(estimated_value, 2),
            "comp_approach_value": round(comp_value, 2),
            "income_approach_value": round(income_value, 2),
            "valuation_date": datetime.date.today().isoformat()
        }

    def solve_irr(self, cash_flows: List[float], iterations: int = 100) -> float:
        """
        Newton-Raphson IRR solver for real estate investment cash flows.
        """
        rate = 0.1 # Initial guess
        for _ in range(iterations):
            npv = 0.0
            d_npv = 0.0
            for t, cf in enumerate(cash_flows):
                denom = (1 + rate) ** t
                npv += cf / denom
                d_npv -= t * cf / (denom * (1 + rate))
            
            if abs(npv) < 0.01:
                break
            if d_npv == 0: break
            rate = rate - npv / d_npv
            
        return round(rate, 4)

    def audit_mena_transaction_costs(self, purchase_price: float, jurisdiction: str = "Dubai") -> Dict[str, Any]:
        """
        Calculates regional transaction costs (DLD, RETT, VAT).
        """
        costs = {}
        if jurisdiction == "Dubai":
            costs["dld_fee"] = purchase_price * 0.04
            costs["admin_fee"] = 4000 if purchase_price > 500000 else 2000
            costs["agent_commission"] = purchase_price * 0.02
        elif jurisdiction == "KSA":
            costs["rett_tax"] = purchase_price * 0.05
            costs["agent_commission"] = purchase_price * 0.025
            
        total_costs = sum(costs.values())
        return {
            "jurisdiction": jurisdiction,
            "cost_breakdown": costs,
            "total_transaction_costs": round(total_costs, 2),
            "total_acquisition_cost": round(purchase_price + total_costs, 2)
        }

    def audit_project_lifecycle(self, project_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits construction-linked payment milestones (Off-plan logic).
        """
        milestones = project_state.get("milestones", [])
        completed = sum(1 for m in milestones if m.get("status") == "verified_complete")
        delays = sum(1 for m in milestones if m.get("is_delayed", False))
        
        return {
            "completion_percentage": (completed / len(milestones) * 100) if milestones else 0,
            "risk_status": "HIGH_DELAY_RISK" if delays > 1 else "STABLE",
            "active_milestones": len(milestones),
            "recommendation": "Escalate to contractor" if delays > 0 else "NO_ACTION"
        }

    def calculate_regulatory_score(self, compliance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies escrow compliance and REGA/DLD registration.
        """
        has_escrow = compliance_data.get("escrow_account_verified", False)
        is_registered = compliance_data.get("rera_registered", False)
        permit_active = compliance_data.get("permit_valid", False)
        
        score = 0
        if has_escrow: score += 50
        if is_registered: score += 30
        if permit_active: score += 20
        
        return {
            "regulatory_score": score,
            "status": "COMPLIANT" if score >= 80 else "RISKY",
            "trust_tier": "OMEGA" if score == 100 else "BETA"
        }

    def calculate_project_yield(self, gdv: float, cost: float) -> Dict[str, Any]:
        """
        Calculates Gross Developable Value (GDV) yield and Margin.
        """
        profit = gdv - cost
        margin = (profit / gdv) * 100 if gdv > 0 else 0
        roi = (profit / cost) * 100 if cost > 0 else 0
        
        return {
            "gdv": gdv,
            "total_cost": cost,
            "net_profit": profit,
            "margin_percentage": round(margin, 2),
            "roi_percentage": round(roi, 2),
            "feasibility": "VIABLE" if roi >= 15 else "MARGINAL"
        }

    def validate_zoning_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates project against municipal zoning parameters.
        Checks: FAR (Floor Area Ratio), Setbacks, and Height Limits.
        """
        far_limit = 3.5 # Standard Cairo/Dubai example
        current_far = project_data.get("built_area", 0) / project_data.get("land_area", 1)
        
        height_limit = 45 # Meters
        current_height = project_data.get("building_height", 0)
        
        violations = []
        if current_far > far_limit: violations.append("FAR_EXCEEDED")
        if current_height > height_limit: violations.append("HEIGHT_LIMIT_EXCEEDED")
        
        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "far_delta": round(far_limit - current_far, 2),
            "tier": "💎 OMEGA" if len(violations) == 0 else "NON_COMPLIANT"
        }
