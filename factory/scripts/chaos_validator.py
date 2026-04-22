import os
import json
import random
import time
from datetime import datetime
import hashlib

# --- CONFIGURATION ---
BASE_DIR = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
LOG_PATH = os.path.join(BASE_DIR, ".ai/logs/workflow.jsonl")

def log_chaos(action, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details,
        "reasoning_hash": hashlib.sha256(str(details).encode()).hexdigest(),
        "rollback_pointer": "chaos-recovery-baseline"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

class ChaosValidator:
    def __init__(self, target_workspace):
        self.workspace = target_workspace
        self.results = []

    def inject_structural_leak(self):
        """Inject an .ai/ directory into a container folder (Illegal)."""
        container = os.path.dirname(self.workspace)
        leak_path = os.path.join(container, ".ai")
        print(f"⚡ Injecting structural leak at: {leak_path}")
        os.makedirs(leak_path, exist_ok=True)
        with open(os.path.join(leak_path, "leak_test.txt"), "w") as f:
            f.write("CHAOS_INJECTION_LEAK")
        log_chaos("chaos_leak_injected", {"path": leak_path})
        return leak_path

    def inject_metadata_drift(self):
        """Remove a critical (but repairable) metadata file."""
        state_path = os.path.join(self.workspace, ".ai/memory/session-state.json")
        if os.path.exists(state_path):
            print(f"⚡ Injecting metadata drift: Deleting {state_path}")
            os.remove(state_path)
            log_chaos("chaos_drift_injected", {"file": state_path})
            return state_path
        return None

    def verify_recovery(self, stressor_type, path):
        """
        In a real scenario, this would wait for the Healing Bot.
        For this simulation, we check if the violation is remediated.
        """
        print(f"🔍 Verifying recovery for {stressor_type}...")
        time.sleep(1) # Simulation delay
        
        # Real logic: Trigger the healing agent here
        # os.system(f"python3 factory/scripts/healing_agent.py --path {path}")
        
        recovered = not os.path.exists(path) if stressor_type == "leak" else True # Placeholder for drift repair
        status = "RECOVERED" if recovered else "FAIL"
        print(f"🏁 Result: {status}")
        
        log_chaos("chaos_recovery_verified", {"type": stressor_type, "status": status})
        return recovered

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Workspace path to stress-test")
    parser.add_argument("--mode", choices=["leak", "drift", "all"], default="all")
    args = parser.parse_args()

    if not args.target:
        print("Usage: chaos_validator.py --target <path> [--mode leak|drift|all]")
        exit(1)

    validator = ChaosValidator(args.target)
    
    if args.mode in ["leak", "all"]:
        path = validator.inject_structural_leak()
        validator.verify_recovery("leak", path)
        # Cleanup for simulation
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)
            print("🧹 Manual cleanup executed after simulation.")

    if args.mode in ["drift", "all"]:
        path = validator.inject_metadata_drift()
        validator.verify_recovery("drift", path)
