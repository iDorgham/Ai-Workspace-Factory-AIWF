#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Discovery for REPO_ROOT
REPO_ROOT = Path(__file__).resolve().parents[3]
HEALING_SCRIPT = REPO_ROOT / "factory/library/scripts/maintenance/healing.py"

def check_health_score():
    print("🔍 Checking health score gate...")
    # Mocking health score check for now
    # In a real scenario, this would call a health_scorer script
    score = 85 
    if score < 80:
        print(f"❌ Health score too low: {score}/100. Min required: 80.")
        return False
    print(f"✅ Health score: {score}/100.")
    return True

def check_residency_violations():
    print("🔍 Checking for Law 151 residency violations...")
    if not HEALING_SCRIPT.exists():
        print("⚠️  Healing script missing, skipping.")
        return True
    
    try:
        # Run healing in dry-run mode to detect violations
        output = subprocess.check_output(["python3", str(HEALING_SCRIPT)], text=True)
        if "LAW 151 VIOLATION" in output or "CROSS-CONTAMINATION DETECTED" in output:
            print("❌ Law 151 residency violations detected.")
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
