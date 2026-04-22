#!/usr/bin/env python3
import shutil
import json
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACES = ROOT / "workspaces"

def migrate_legacy():
    print("🚀 Starting Legacy Workspace Migration to v2.1...")
    clients_dir = WORKSPACES / "clients"
    clients_dir.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    memory_injected_count = 0
    
    # 1. Structural Migration (moving flat folders)
    for item in WORKSPACES.iterdir():
        if item.is_dir() and item.name not in ["clients", "personal", "README.md"]:
            client_name = item.name
            target_client_dir = clients_dir / client_name
            target_client_dir.mkdir(parents=True, exist_ok=True)
            project_dir = target_client_dir / f"001_{client_name}"
            
            print(f"📦 Migrating Folder: {client_name} -> {project_dir}")
            shutil.move(str(item), str(project_dir))
            
            if not (target_client_dir / "metadata.json").exists():
                (target_client_dir / "metadata.json").write_text(json.dumps({"client": client_name}))
            moved_count += 1

    # Loop existing clients to fix structures
    for client_folder in clients_dir.iterdir():
        if client_folder.is_dir():
            for project_folder in client_folder.iterdir():
                # 2. Wrap un-nested legacy projects
                if project_folder.is_dir() and not project_folder.name.startswith("001_"):
                    new_project_path = client_folder / f"001_{project_folder.name}"
                    print(f"📦 Wrapping nested project: {project_folder.name} -> 001_...")
                    shutil.move(str(project_folder), str(new_project_path))
                    moved_count += 1
                    project_folder = new_project_path # updated ref for step 3

                # 3. Check for Dashboard Memory (V2.1 compliance)
                if project_folder.is_dir() and project_folder.name.startswith("001_"):
                    dash_dir = project_folder / ".ai" / "dashboard"
                    memory_file = dash_dir / "memory.json"
                    
                    if not memory_file.exists():
                        dash_dir.mkdir(parents=True, exist_ok=True)
                        fallback_memory = {
                            "project_id": project_folder.name,
                            "client_id": client_folder.name,
                            "status": "Archival/Legacy",
                            "health": 50,
                            "progress_percentage": 0,
                            "phases": [{"name": "Legacy Import", "status": "pending"}],
                            "tasks": [],
                            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
                        }
                        memory_file.write_text(json.dumps(fallback_memory, indent=2))
                        print(f"💉 Injected Dashboard Memory into: {project_folder.name}")
                        memory_injected_count += 1
                    
    print(f"✅ Migration Complete. {moved_count} structures moved. {memory_injected_count} memory states injected.")

if __name__ == "__main__":
    migrate_legacy()
