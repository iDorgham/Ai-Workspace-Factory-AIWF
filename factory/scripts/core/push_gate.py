#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Discovery for REPO_ROOT
REPO_ROOT = Path(__file__).resolve().parents[3]
HEALING_SCRIPT = REPO_ROOT / "factory/library/scripts/maintenance/healing.py"

def check_health_score():
    print("Checking health score gate...")
    health_script = REPO_ROOT / "factory" / "scripts" / "maintenance" / "health_scorer.py"
    if not health_script.exists():
        print("Health scorer script missing. Failing closed.")
        return False
    try:
        output = subprocess.check_output(["python3", str(health_script)], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        print(f"Health scorer execution failed: {exc}")
        return False

    score = None
    for line in output.splitlines():
        digits = "".join(ch for ch in line if ch.isdigit())
        if "/" in line and digits:
            try:
                score = int(digits[:3])
                break
            except ValueError:
                continue

    if score is None:
        print("Unable to parse health score output. Failing closed.")
        return False
    if score < 80:
        print(f"Health score too low: {score}/100. Min required: 80.")
        return False
    print(f"Health score: {score}/100.")
    return True

def check_residency_violations():
    print("Checking for Law 151 residency violations...")
    if not HEALING_SCRIPT.exists():
        print("Healing script missing. Failing closed.")
        return False
    
    try:
        # Run healing in dry-run mode to detect violations
        output = subprocess.check_output(["python3", str(HEALING_SCRIPT)], text=True)
        if "LAW 151 VIOLATION" in output or "CROSS-CONTAMINATION DETECTED" in output:
            print("Law 151 residency violations detected.")
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    success = True
    if not check_health_score(): success = False
    if not check_residency_violations(): success = False
    
    if not success:
        print("\n🛑 Push gate FAILED. Compliance block active.")
        sys.exit(1)
    
    print("\n✅ Push gate PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
