import json
import os

def validate_registry():
    registry_path = ".ai/agents/registry.json"
    if not os.path.exists(registry_path):
        print(f"[ERROR] Registry not found at {registry_path}")
        return False

    with open(registry_path, 'r') as f:
        data = json.load(f)

    # Validate structure
    agents_data = data.get('agents', {})
    for tier, agents in agents_data.items():
        for name, meta in agents.items():
            if 'sovereign_tier' not in meta:
                print(f"[FAIL] Agent {name} missing sovereign_tier")
                return False
            if 'compliance_id' not in meta:
                print(f"[FAIL] Agent {name} missing compliance_id")
                return False

    print("[SUCCESS] Agent Registry v13.0.0 OMEGA validated (Dependency-Free).")
    return True

if __name__ == "__main__":
    validate_registry()
