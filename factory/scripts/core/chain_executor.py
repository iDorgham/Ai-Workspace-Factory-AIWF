import sys
import subprocess
import time
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

def generate_reasoning_hash(session_id="SESS-001"):
    timestamp = str(time.time())
    data = f"{session_id}-{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:12]

def execute_step(name, command):
    print(f"🚀 [STEP: {name}] Executing: {command}")
    try:
        subprocess.check_call(command, shell=True)
        print(f"✅ [STEP: {name}] SUCCESS.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ [STEP: {name}] FAILED with code {e.returncode}.")
        return False

def execute_commit_fsm(message):
    reasoning_hash = generate_reasoning_hash()
    full_message = f"{message} [Reasoning: {reasoning_hash}] [Law151: certified]"
    
    print(f"[*] Initializing Sovereign Commit FSM | Hash: {reasoning_hash}")
    
    # Step 1: Integrity Auditor
    if not execute_step("integrity_auditor", "python3 factory/library/scripts/maintenance/audit_path_integrity.py"):
        print("🛑 FSM Blocked: Integrity violation.")
        return False
    
    # Step 2: Documentation Architect (Auto-update README/Dashboard)
    if not execute_step("documentation_architect", "python3 factory/library/scripts/intelligence/proactive_brainstorm_trigger.py"):
         print("⚠️  Warning: Documentation architect failed, proceeding with caution.")
    
    # Step 3: Registry Guardian (Actual Commit)
    commit_cmd = f'git commit -m "{full_message}"'
    if not execute_step("registry_guardian", commit_cmd):
        print("🛑 FSM Blocked: Commit failed.")
        return False
        
    print(f"\n[+] Sovereign Commit COMPLETED. Reasoning: {reasoning_hash}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chain_executor.py \"Commit message\"")
        sys.exit(1)
    
    msg = sys.argv[1]
    if not execute_commit_fsm(msg):
        sys.exit(1)
