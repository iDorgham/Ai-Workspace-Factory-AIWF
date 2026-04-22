import json
import os
from datetime import datetime

AGGREGATED_STATE = "master/.ai/memory/aggregated-state.json"
SYNERGY_REPORT = "master/.ai/memory/synergy-report.json"

def analyze_synergies():
    if not os.path.exists(AGGREGATED_STATE):
        print(f"Error: {AGGREGATED_STATE} not found.")
        return

    with open(AGGREGATED_STATE, 'r') as f:
        state = json.load(f)

    clients = state.get("clients", {})
    synergies = []

    # Synergy Logic: Industry Convergence
    # 1. Infrastructure (Energy/AEC) + Islamic Finance
    # 2. HealthTech + Legal (Compliance)
    # 3. GovTech + All (Institutional Integration)

    for slug, data in clients.items():
        roi = data.get("strategic_roi", {})
        pos = roi.get("market_position", "")
        
        # Check for Infrastructure + Finance Synergy
        if "Infrastructure" in pos or "Dominant-AEC" in pos:
            if any("Sharia" in c.get("strategic_roi", {}).get("market_position", "") for c in clients.values()):
                synergies.append({
                    "id": f"syn_{slug}_finance",
                    "type": "FINANCIAL_CONVERGENCE",
                    "source": slug,
                    "target": "02_mena-legal",
                    "opportunity": "Optimize infrastructure debt via Sharia-compliant (Murabaha) instruments.",
                    "impact": "High"
                })

        # Check for HealthTech + Legal
        if "Elite-Research" in pos:
            synergies.append({
                "id": f"syn_{slug}_legal",
                "type": "COMPLIANCE_CONVERGENCE",
                "source": slug,
                "target": "02_mena-legal",
                "opportunity": "Unified Clinical Trial Regulatory Framework across MENA jurisdictions.",
                "impact": "Stable"
            })

        # Check for GovTech + All
        if "National-Transformation" in pos:
            synergies.append({
                "id": "syn_gov_all",
                "type": "GOVERNANCE_CONVERGENCE",
                "source": slug,
                "target": "PORTFOLIO",
                "opportunity": "Institutional integration of all enterprise nodes into the national digital hub.",
                "impact": "Critical"
            })

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_synergies": len(synergies),
        "active_opportunities": synergies,
        "master_health_score": state.get("master_health_score", 0)
    }

    with open(SYNERGY_REPORT, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Synergy analysis complete. Found {len(synergies)} opportunities. Report saved to {SYNERGY_REPORT}.")

if __name__ == "__main__":
    analyze_synergies()
