import os
import shutil
import json
import hashlib
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
LIBRARY_AGENTS = os.path.join(BASE_DIR, "factory/library/agents")
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
LOG_PATH = os.path.join(BASE_DIR, ".ai/logs/workflow.jsonl")

def log_sync(action, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details,
        "reasoning_hash": hashlib.sha256(str(details).encode()).hexdigest(),
        "rollback_pointer": "hot-sync-rollback"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def sync_workspace(workspace_path, dry_run=False):
    updates = []
    # Identify Managed Agents in the workspace
    ws_agents_dir = os.path.join(workspace_path, ".ai/agents")
    if not os.path.exists(ws_agents_dir):
        return []

    # Map Library Agents to Workspace Agents
    # For this implementation, we assume a standard mapping
    for agent_name in os.listdir(LIBRARY_AGENTS):
        lib_agent_path = os.path.join(LIBRARY_AGENTS, agent_name, "AGENT.md")
        ws_agent_path = os.path.join(ws_agents_dir, agent_name, "AGENT.md")
        
        if os.path.exists(ws_agent_path):
            lib_hash = get_file_hash(lib_agent_path)
            ws_hash = get_file_hash(ws_agent_path)
            
            if lib_hash != ws_hash:
                updates.append({
                    "agent": agent_name,
                    "source": lib_agent_path,
                    "target": ws_agent_path,
                    "type": "update"
                })

    if not dry_run:
        for update in updates:
            # Safe Backup
            backup_path = update["target"] + ".hot-bak"
            shutil.copy2(update["target"], backup_path)
            # Apply Update
            shutil.copy2(update["source"], update["target"])
            log_sync("agent_hot_sync_applied", {"workspace": workspace_path, "agent": update["agent"]})
            
    return updates

def run_hot_sync(scope="all", dry_run=False):
    all_updates = {}
    
    # Iterate through all workspaces
    for container in ["01-Personal", "02-Clients"]:
        c_path = os.path.join(WORKSPACES_DIR, container)
        if not os.path.exists(c_path): continue
        
        # Deep walk to find .ai folders (Sovereign Projects)
        for root, dirs, files in os.walk(c_path):
            if ".ai" in dirs:
                project_path = root
                ws_updates = sync_workspace(project_path, dry_run)
                if ws_updates:
                    all_updates[project_path] = ws_updates
                # Don't recurse into .ai
                dirs.remove(".ai")
                
    return all_updates

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--safe", action="store_true", help="Apply updates with backups")
    parser.add_argument("--dry-run", action="store_true", help="Check for updates without applying")
    args = parser.parse_args()

    results = run_hot_sync(dry_run=not args.safe)
    print(json.dumps(results, indent=2))
