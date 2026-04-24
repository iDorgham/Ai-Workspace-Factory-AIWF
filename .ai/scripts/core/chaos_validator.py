#!/usr/bin/env python3
import os
import sys
import time
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / ".ai" / "logs" / "chaos-scaffolding.md"

def generate_reasoning_hash(agent_id="CV"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    nonce = os.urandom(2).hex()
    return f"[{agent_id}-{timestamp}-{nonce}]"

def log_event(message, hash_id):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_FILE, "a") as f:
        f.write(f"- **{timestamp}** {hash_id}: {message}\n")

def inject_chaos(level="low"):
    ws_root = ROOT / "workspaces"
    clients_dir = ws_root / "clients"
    
    if not clients_dir.exists():
        print("❌ No workspaces found to inject chaos.")
        return

    # Select a random project
    all_projects = list(clients_dir.glob("**/00*"))
    if not all_projects:
        print("❌ No project nodes found.")
        return
        
    target_project = random.choice(all_projects)
    client_folder = target_project.parent
    
    hash_id = generate_reasoning_hash()
    
    if level == "low":
        # Stressor 1: Metadata Pollution
        rogue_file = client_folder / f"chaos_rogue_{random.randint(100, 999)}.txt"
        rogue_file.touch()
        msg = f"Injected LOW chaos: Created rogue file '{rogue_file.name}' in client '{client_folder.name}'"
        print(f"🔥 {msg}")
        log_event(msg, hash_id)
        
    elif level == "medium":
        # Stressor 2: Sovereignty Breach (Missing .ai)
        ai_dir = target_project / ".ai"
        if ai_dir.exists():
            # Rename it instead of deleting for safety
            backup_ai = target_project / ".ai_chaos_backup"
            ai_dir.rename(backup_ai)
            msg = f"Injected MEDIUM chaos: Sabotaged .ai/ folder in project '{target_project.name}'"
            print(f"🔥 {msg}")
            log_event(msg, hash_id)

    return target_project

def main():
    level = "low"
    for arg in sys.argv:
        if arg in ["low", "medium", "high"]:
            level = arg
            
    if not LOG_FILE.parent.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            f.write("# 🧪 CHAOS SCAFFOLDING & RECOVERY LOGS\n\n")

    print(f"🎭 Chaos Validator initiating '{level}' stress test...")
    target = inject_chaos(level)
    
    if target:
        print(f"\n✅ Chaos injected. Target: {target.name}")
        print("🛠️  Run '/heal check --auto' to verify Antifragile recovery.")

if __name__ == "__main__":
    main()
