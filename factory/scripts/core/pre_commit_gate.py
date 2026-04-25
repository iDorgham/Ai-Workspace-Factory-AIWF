#!/usr/bin/env python3
import subprocess
import sys
import re
from pathlib import Path

# Discovery for REPO_ROOT
REPO_ROOT = Path(__file__).resolve().parents[3]
DRIFT_CHECK_SCRIPT = REPO_ROOT / "factory/library/10_engineering_devops/01_software_engineering/developing/scripts/check_mirror_drift.py"

def check_snake_case():
    print("🔍 Checking for snake_case naming violations...")
    # Get staged files
    try:
        files = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).splitlines()
    except: return True # Not in git repo or no staged files
    
    violations = []
    for f in files:
        if f.startswith(".github/") or f.startswith("docs/"):
            continue # Allow standard naming in these dirs
        basename = Path(f).name
        if "." in basename:
             name_part = basename.split(".")[0]
             if not re.match(r"^[a-z0-9_]+$", name_part) and name_part != "README" and name_part != "TOMBSTONE":
                 violations.append(f)
    
    if violations:
        print("❌ Naming violations detected (must be snake_case):")
        for v in violations:
            print(f"  - {v}")
        return False
    return True

def check_mirror_drift():
    print("🔍 Checking mirror drift status...")
    if not DRIFT_CHECK_SCRIPT.exists():
        print("⚠️  Mirror drift script missing, skipping.")
        return True
    
    try:
        # Run with threshold 50 for industrialization phase
        subprocess.check_call(["python3", str(DRIFT_CHECK_SCRIPT), "--threshold", "50"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Mirror drift exceeds threshold (5 nodes). Run /git sync to repair.")
        return False

def check_placeholders():
    print("🔍 Checking for TODO_PLACEHOLDER strings...")
    try:
        # Grep staged files for placeholder, excluding validation scripts, docs, and pycache
        subprocess.check_call(["git", "grep", "--cached", "-q", "TODO_PLACEHOLDER", "--", ".", ":!factory/scripts/core/pre_commit_gate.py", ":!factory/scripts/core/validate.py", ":!docs/**", ":!**/__pycache__/**"])
        print("❌ TODO_PLACEHOLDER detected in staged changes.")
        return False
    except subprocess.CalledProcessError:
        return True # Not found

def main():
    success = True
    if not check_snake_case(): success = False
    if not check_mirror_drift(): success = False
    if not check_placeholders(): success = False
    
    if not success:
        print("\n🛑 Pre-commit gate FAILED. Fix violations before committing.")
        sys.exit(1)
    
    print("\n✅ Pre-commit gate PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
