#!/usr/bin/env python3
import json
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
AGGREGATED_STATE_PATH = ROOT / "master" / ".ai" / "memory" / "aggregated-state.json"
WORKSPACES_DIR = ROOT / "workspaces"

def get_all_workspaces():
    workspaces = []
    # Search in clients/
    clients_dir = WORKSPACES_DIR / "clients"
    if clients_dir.exists():
        for client in clients_dir.iterdir():
            if client.is_dir():
                for project in client.iterdir():
                    if project.is_dir() and (project / ".ai").exists():
                        workspaces.append({
                            "type": "client",
                            "client": client.name,
                            "project": project.name,
                            "path": project
                        })
    
    # Search in personal/
    personal_dir = WORKSPACES_DIR / "personal"
    if personal_dir.exists():
        for project in personal_dir.iterdir():
            if project.is_dir() and (project / ".ai").exists():
                workspaces.append({
                    "type": "personal",
                    "project": project.name,
                    "path": project
                })
    
    return workspaces

def sync_all():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting aggregation sync...")
    
    if not AGGREGATED_STATE_PATH.exists():
        state = {"master_health_score": 100, "clients": {}, "personal": {}, "last_updated": ""}
    else:
        with open(AGGREGATED_STATE_PATH, "r") as f:
            state = json.load(f)

    workspaces = get_all_workspaces()
    
    for ws in workspaces:
        ws_state_path = ws["path"] / ".ai" / "memory" / "state.json"
        
        # If child state exists, read it
        if ws_state_path.exists():
            with open(ws_state_path, "r") as f:
                child_data = json.load(f)
        else:
            # Default stub if state.json doesn't exist yet
            child_data = {"status": "active", "health": 100, "tasks_remaining": []}

        if ws["type"] == "client":
            client_name = ws["client"]
            if client_name not in state["clients"]:
                state["clients"][client_name] = {"name": client_name, "projects": {}}
            state["clients"][client_name]["projects"][ws["project"]] = child_data
        else:
            state["personal"][ws["project"]] = child_data

    # Aggregate Strategic ROI Memory
    clients_memory_dir = ROOT / "master" / ".ai" / "memory" / "clients"
    if clients_memory_dir.exists():
        for client_file in clients_memory_dir.glob("*.json"):
            with open(client_file, "r") as f:
                memory_data = json.load(f)
            c_slug = client_file.stem
            if c_slug in state["clients"]:
                # Strategic Tagging Logic
                roi = memory_data.get("roi_index", 1.0)
                if roi >= 1.4:
                    tag = "High-Yield"
                elif roi < 1.1:
                    tag = "At-Risk"
                else:
                    tag = "Stable"
                
                memory_data["strategic_tag"] = tag
                state["clients"][c_slug]["strategic_roi"] = memory_data

    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    with open(AGGREGATED_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"Sync complete. Aggregated {len(workspaces)} workspaces.")

if __name__ == "__main__":
    sync_all()
