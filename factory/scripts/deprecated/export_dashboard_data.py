# TOMBSTONED: 2026-04-25 | Reason: DEPRECATED | Successor: N/A | Do not import.
import os
import json
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
LOG_PATH = os.path.join(BASE_DIR, ".ai/logs/workflow.jsonl")
REPORT_PATH = os.path.join(BASE_DIR, ".ai/logs/health-audit-report.md")
EXPORT_PATH = os.path.join(BASE_DIR, "dashboard/data.json")

def get_health_score():
    if not os.path.exists(REPORT_PATH):
        return 0.0
    with open(REPORT_PATH, "r") as f:
        content = f.read()
        # Simple extraction from markdown
        import re
        match = re.search(r"Global Health Score\*\*: ([\d\.]+)/100", content)
        if match:
            return float(match.group(1))
    return 0.0

def get_ledger():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()
    logs = [json.loads(line) for line in lines[-10:]]
    ledger = []
    for log in reversed(logs):
        ledger.append({
            "timestamp": log.get("timestamp", ""),
            "action": log.get("action") or log.get("command") or "Action",
            "hash": (log.get("reasoning_hash") or log.get("status") or "N/A")[:12]
        })
    return ledger

def get_topology():
    topology = []
    for container in ["01-Personal", "02-Clients"]:
        c_path = os.path.join(WORKSPACES_DIR, container)
        projects = []
        if os.path.exists(c_path):
            for d in sorted(os.listdir(c_path)):
                if os.path.isdir(os.path.join(c_path, d)):
                    projects.append({
                        "name": d,
                        "status": "Active" if os.path.exists(os.path.join(c_path, d, ".ai")) else "Container"
                    })
        topology.append({"name": container, "projects": projects})
    return topology

def export_data():
    data = {
        "health": {"score": get_health_score()},
        "ledger": get_ledger(),
        "topology": get_topology(),
        "last_update": datetime.now().isoformat()
    }
    with open(EXPORT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Dashboard data exported to {EXPORT_PATH}")

if __name__ == "__main__":
    export_data()
