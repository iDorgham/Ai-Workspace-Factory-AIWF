#!/usr/bin/env python3
import os
import sys
import time
import shutil
from pathlib import Path
from audit_path_integrity import audit_path_integrity

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / ".ai" / "logs" / "healing-bot.md"

def generate_reasoning_hash(agent_id="HB"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    nonce = os.urandom(2).hex()
    return f"[{agent_id}-{timestamp}-{nonce}]"

def log_event(message, hash_id):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_FILE, "a") as f:
        f.write(f"- **{timestamp}** {hash_id}: {message}\n")

def remediate(workspaces_root: str, auto: bool = False):
    root = Path(workspaces_root)
    violations = []
    
    # We'll use a modified version of the audit logic to get the raw list
    # For now, let's re-implement the parsing logic here to handle remediation
    
    clients_dir = root / "clients"
    if not clients_dir.exists():
        return

    for client_folder in clients_dir.iterdir():
        if not client_folder.is_dir(): continue
        
        # FR-2.1: Metadata Pollution
        allowed = ["metadata.json", "README.md", "dashboard", ".DS_Store"]
        for item in client_folder.iterdir():
            if not item.is_dir() and item.name not in allowed:
                msg = f"Removing illegal file '{item.name}' from client '{client_folder.name}'"
                print(f"🛠️  {msg}")
                hash_id = generate_reasoning_hash()
                if auto:
                    item.unlink()
                    log_event(msg, hash_id)
            elif item.is_dir() and not (item.name.startswith("00") and "_" in item.name) and item.name != "dashboard":
                msg = f"Removing illegal directory '{item.name}' from client '{client_folder.name}'"
                print(f"🛠️  {msg}")
                hash_id = generate_reasoning_hash()
                if auto:
                    shutil.rmtree(item)
                    log_event(msg, hash_id)

        # FR-2.2: Sovereignty Violations
        for project_folder in client_folder.iterdir():
            if project_folder.is_dir() and project_folder.name.startswith("00"):
                if not (project_folder / ".ai").exists():
                    msg = f"Restoring missing .ai/ folder in project '{project_folder.name}'"
                    print(f"🛠️  {msg}")
                    hash_id = generate_reasoning_hash()
                    if auto:
                        (project_folder / ".ai").mkdir(parents=True, exist_ok=True)
                        # Minimal scaffolding
                        (project_folder / ".ai" / "agents").mkdir(exist_ok=True)
                        (project_folder / ".ai" / "skills").mkdir(exist_ok=True)
                        (project_folder / ".ai" / "memory").mkdir(exist_ok=True)
                        log_event(msg, hash_id)

                if not (project_folder / "dashboard").exists():
                    msg = f"Restoring missing dashboard/ folder in project '{project_folder.name}'"
                    print(f"🛠️  {msg}")
                    hash_id = generate_reasoning_hash()
                    if auto:
                        (project_folder / "dashboard").mkdir(parents=True, exist_ok=True)
                        log_event(msg, hash_id)

def main():
    ws_root = str(ROOT / "workspaces")
    auto = "--auto" in sys.argv
    
    if not LOG_FILE.parent.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            f.write("# 📑 HEALING BOT APPEND-ONLY REPAIR LOGS\n\n")

    print(f"🤖 Healing Bot starting audit on '{ws_root}'...")
    remediate(ws_root, auto)
    
    if not auto:
        print("\n⚠️  Dry-run complete. Use '--auto' to execute remediation.")
    else:
        print("\n✅ Remediation complete. Check '.ai/logs/healing-bot.md' for details.")

if __name__ == "__main__":
    main()
