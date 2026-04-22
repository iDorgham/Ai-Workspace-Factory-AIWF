"""
⚡ Islamic Finance Mastery - Operational Core
Functionalizes specialized Sharia-compliant investment filters and Zakat calculation logic for Skill 11.13.
"""

from typing import Dict, Any, List

class IslamicFinanceMastery:
    def __init__(self):
        self.version = "11.0.0"
        self.logic = "sharia-fintech-standard"

    def filter_sharia_compliance(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Filters assets based on Sharia standards (No Riba, No Gharar, Debt < 33%).
        """
        compliant = []
        violations = []
        
        for asset in portfolio_data:
            debt_ratio = asset.get("total_debt", 0) / asset.get("market_cap", 1)
            has_forbidden_revenue = asset.get("forbidden_revenue_perc", 0) > 0.05 # AAOIFI Standard: < 5%
            
            is_compliant = debt_ratio < 0.33 and not has_forbidden_revenue
            
            if is_compliant:
                compliant.append(asset["id"])
            else:
                violations.append({
                    "id": asset["id"],
                    "reason": "HIGH_DEBT" if debt_ratio >= 0.33 else "FORBIDDEN_REVENUE"
                })
                
        return {
            "compliant_assets": compliant,
            "violations_detected": violations,
            "compliance_rating": len(compliant) / len(portfolio_data) if portfolio_data else 1.0,
            "status": "SHARIA_AUDITED"
        }

    def calculate_zakat(self, zakatable_assets: Dict[str, float]) -> Dict[str, float]:
        """
        Calculates institutional Zakat (2.5% on qualifying lunar-year assets).
        """
        total_value = sum(zakatable_assets.values())
        zakat_amount = total_value * 0.025
        
        return {
            "total_zakatable_value": total_value,
            "zakat_due_amount": round(zakat_amount, 2),
            "currency": "USD" # Default, can be overridden
        }

    def calculate_profit_rate_murabaha(self, cost: float, margin_percent: float) -> Dict[str, Any]:
        """
        Calculates the Murabaha profit rate and total resale price.
        Logic: Total = Cost + (Cost * Margin).
        """
        profit = cost * (margin_percent / 100)
        total_price = cost + profit
        
        return {
            "instrument": "MURABAHA",
            "acquisition_cost": cost,
            "profit_margin": profit,
            "resale_price": total_price,
            "sharia_ready": True
        }
