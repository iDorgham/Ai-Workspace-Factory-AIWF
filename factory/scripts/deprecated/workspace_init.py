# TOMBSTONED: 2026-04-25 | Reason: DEPRECATED | Successor: N/A | Do not import.
import os
import json
import re
import sys
from datetime import datetime
import hashlib

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
LOG_PATH = os.path.join(BASE_DIR, ".ai/logs/workflow.jsonl")

def log_action(action, details, hash=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details,
        "reasoning_hash": hash or hashlib.sha256(str(details).encode()).hexdigest(),
        "rollback_pointer": "v6.0.0-baseline"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_state_path(project_path):
    return os.path.join(project_path, ".ai/memory/session-state.json")

def load_state(project_path):
    path = get_state_path(project_path)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_state(project_path, state):
    path = get_state_path(project_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def advance_step(project_path, input_data=None):
    state = load_state(project_path)
    if not state:
        return {"error": "No active session found for this path."}

    current_step = state.get("step", 1)
    
    # --- STEP 1: Vision Capture ---
    if current_step == 1:
        if not input_data:
            return {"step": 1, "prompt": "Provide a 1-2 sentence vision or core objective."}
        state["vision"] = input_data
        state["step"] = 2
        state["status"] = "CAPTURING_CONTEXT"
        save_state(project_path, state)
        return {"step": 2, "prompt": "Add tech stack, audience, brand, or constraints. (Reply 'skip' to proceed.)"}

    # --- STEP 2: Context Injection ---
    if current_step == 2:
        if input_data and input_data.lower() != "skip":
            state["context"] = input_data
        state["step"] = 3
        state["status"] = "SELECTING_PRD_MODE"
        save_state(project_path, state)
        return {"step": 3, "prompt": "Choose PRD Mode: [A] Direct [B] Generate [C] Brainstorm"}

    # --- STEP 3: PRD Strategy ---
    if current_step == 3:
        if not input_data or input_data.upper() not in ["A", "B", "C"]:
            return {"step": 3, "prompt": "Invalid choice. Select [A], [B], or [C]."}
        state["prd_mode"] = input_data.upper()
        state["step"] = 4
        state["status"] = "WAITING_FOR_PRD"
        save_state(project_path, state)
        
        # Internal Routing logic would trigger Swarm Router here
        return {"step": 4, "prompt": f"PRD Mode '{state['prd_mode']}' initialized. Upload/Drafting in progress. Approval required next."}

    # --- STEP 4: Omega Gate Approval ---
    if current_step == 4:
        if input_data and input_data.lower() in ["y", "approve", "yes"]:
            state["step"] = 5
            state["status"] = "PROVISIONING_DIRECTORIES"
            save_state(project_path, state)
            log_action("omega_gate_approved", {"path": project_path})
            return {"step": 5, "prompt": "PRD Approved. Resolving profile and injecting directories..."}
        return {"step": 4, "prompt": "Waiting for Omega Gate Approval (y/n/revise)."}

    # --- STEP 5: Finalization ---
    if current_step == 5:
        state["step"] = 6
        state["status"] = "COMPLETE"
        save_state(project_path, state)
        log_action("workspace_provisioning_complete", {"path": project_path})
        return {"step": 6, "status": "COMPLETE", "msg": "✅ Workspace provisioned successfully."}

    return state

def generate_slug(name):
    clean = re.sub(r'[^a-z0-9]', '-', name.lower()).strip('-')
    return f"{clean}"

def get_next_id(container_path):
    if not os.path.exists(container_path):
        os.makedirs(container_path, exist_ok=True)
        return "001"
    dirs = [d for d in os.listdir(container_path) if os.path.isdir(os.path.join(container_path, d))]
    ids = [int(re.match(r'^(\d+)_', d).group(1)) for d in dirs if re.match(r'^(\d+)_', d)]
    return f"{max(ids) + 1:03d}" if ids else "001"

def init_workspace(target_type, container_name, project_name):
    slug = generate_slug(project_name)
    if target_type == "personal":
        container_path = os.path.join(WORKSPACES_DIR, "01-Personal")
    else:
        container_path = os.path.join(WORKSPACES_DIR, "02-Clients", generate_slug(container_name))
    
    project_id = get_next_id(container_path)
    project_dir = f"{project_id}_{slug}"
    full_path = os.path.join(container_path, project_dir)
    
    os.makedirs(os.path.join(full_path, ".ai/memory"), exist_ok=True)
    os.makedirs(os.path.join(full_path, "docs"), exist_ok=True)
    
    state = {
        "project_id": project_id,
        "project_name": project_name,
        "slug": slug,
        "path": full_path,
        "step": 1,
        "status": "INITIALIZING"
    }
    save_state(full_path, state)
    log_action("workspace_provisioning_started", {"path": full_path, "type": target_type})
    return state

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", nargs="+", help="type project_name [client_name]")
    parser.add_argument("--resume", help="Path to project workspace")
    parser.add_argument("--input", help="User input for the current step")
    args = parser.parse_args()

    if args.init:
        target_type = args.init[0]
        project_name = args.init[1]
        client_name = args.init[2] if len(args.init) > 2 else None
        state = init_workspace(target_type, client_name, project_name)
        print(json.dumps({"step": 1, "prompt": "Provide a 1-2 sentence vision or core objective.", "path": state["path"]}, indent=2))
    elif args.resume:
        result = advance_step(args.resume, args.input)
        print(json.dumps(result, indent=2))
