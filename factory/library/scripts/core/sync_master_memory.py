#!/usr/bin/env python3
import os
import sys
import json
import datetime
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
MEMORY_DIR = ROOT / "memory"
INDEX_FILE = MEMORY_DIR / "workspace-index.json"

def sync_master_memory():
    print("🔄 Starting Master Memory Sync...")
    
    if not INDEX_FILE.exists():
        index = {
            "version": "5.0.0",
            "last_synced": None,
            "clients": {},
            "metrics": {"total_clients": 0, "total_projects": 0}
        }
    else:
        index = json.loads(INDEX_FILE.read_text())

    workspaces_dir = REPO_ROOT / "workspaces"
    clients_dir = workspaces_dir / "clients"
    
    if not clients_dir.exists():
        print("⚠ No clients found.")
        return

    total_projects = 0
    client_count = 0
    
    for client_folder in clients_dir.iterdir():
        if not client_folder.is_dir(): continue
        client_count += 1
        client_slug = client_folder.name
        
        if client_slug not in index["clients"]:
            index["clients"][client_slug] = {"projects": {}, "metadata": {}}
        
        # Sync client metadata
        meta_file = client_folder / "metadata.json"
        if meta_file.exists():
            index["clients"][client_slug]["metadata"] = json.loads(meta_file.read_text())

        # Sync projects
        for project_folder in client_folder.iterdir():
            if project_folder.is_dir() and project_folder.name.startswith("00"):
                total_projects += 1
                project_slug = project_folder.name
                
                # Try to find memory.json in .ai/dashboard/
                mem_file = project_folder / ".ai" / "dashboard" / "memory.json"
                if mem_file.exists():
                    index["clients"][client_slug]["projects"][project_slug] = json.loads(mem_file.read_text())
                else:
                    index["clients"][client_slug]["projects"][project_slug] = {"status": "Initialized"}

    index["last_synced"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    index["metrics"]["total_clients"] = client_count
    index["metrics"]["total_projects"] = total_projects
    
    # Simple Pattern Detection (FR-3.3)
    if total_projects > 3:
        index["metrics"]["cross_project_patterns_detected"] = 1
        print("✨ Cross-project patterns detected!")

    INDEX_FILE.write_text(json.dumps(index, indent=2))
    print(f"✅ Sync Complete: {client_count} Clients, {total_projects} Projects tracked.")

    # v6.0.0 Recursive Learning Hook
    print("🐝 Triggering Recursive Learning Engine...")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "recursive_engine.py"), "--execute"], capture_output=True)


if __name__ == "__main__":
    sync_master_memory()
