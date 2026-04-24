"""
⚡ Energy & Renewables Mastery - Operational Core
LCOE Solver, Solar Yield Estimation, and Grid Stability Compliance Logic.
"""

from typing import Dict, Any, List
import math

class EnergyRenewablesMastery:
    def __init__(self):
        self.version = "11.0.0"
        self.logic = "energy-infrastructure-standard"

    def calculate_lcoe(self, capex: float, opex: float, annual_yield_mwh: float, discount_rate: float, lifespan_years: int = 25) -> Dict[str, Any]:
        """
        Calculates the Levelized Cost of Energy (LCOE) over the project lifecycle.
        LCOE = sum(costs / (1+r)^t) / sum(yield / (1+r)^t)
        """
        total_discounted_cost = capex
        total_discounted_yield = 0.0
        
        for t in range(1, lifespan_years + 1):
            discount_factor = (1 + discount_rate) ** t
            total_discounted_cost += opex / discount_factor
            total_discounted_yield += annual_yield_mwh / discount_factor
            
        lcoe = total_discounted_cost / total_discounted_yield if total_discounted_yield > 0 else 0
        
        return {
            "lcoe_per_mwh": round(lcoe, 2),
            "currency": "EGP",
            "tier": "💎 OMEGA" if lcoe < 50 else "INDUSTRIAL",
            "lifecycle_yield_mwh": round(total_discounted_yield, 2)
        }

    def estimate_solar_yield(self, dc_capacity_kwp: float, ghi: float, pr: float = 0.8) -> float:
        """
        Estimates annual MWh yield for a solar PV plant.
        Yield = Capacity * GHI * Performance Ratio (PR)
        """
        annual_yield_kwh = dc_capacity_kwp * ghi * pr
        return round(annual_yield_kwh / 1000, 2) # Return in MWh

    def validate_grid_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates grid synchronization parameters (Frequency, Voltage, THD).
        """
        target_freq = 50.0 # Hz
        current_freq = project_data.get("measured_frequency", 0.0)
        
        thd_limit = 0.05 # 5% Total Harmonic Distortion
        current_thd = project_data.get("measured_thd", 0.0)
        
        violations = []
        if abs(target_freq - current_freq) > 0.1: violations.append("FREQUENCY_MISMATCH")
        if current_thd > thd_limit: violations.append("THD_EXCEEDED")
        
        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "sync_status": "LOCKED" if len(violations) == 0 else "TRIPPED",
            "score": 100 - (len(violations) * 50)
        }
