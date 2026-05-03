# TOMBSTONED: 2026-04-25 | Reason: DEPRECATED | Successor: N/A | Do not import.
import os
import json
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
LOG_PATH = os.path.join(BASE_DIR, ".ai/logs/workflow.jsonl")
HEALING_LOG = os.path.join(BASE_DIR, ".ai/logs/healing-bot.md")
SKILL_DIR = os.path.join(BASE_DIR, ".ai/memory/skill-memory")

def get_last_n_logs(n=5):
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines[-n:]]

def render_structure_map():
    print("🌲 WORKSPACE TOPOLOGY (v6.0.0-VALIDATED)")
    for container in ["01-Personal", "02-Clients"]:
        c_path = os.path.join(WORKSPACES_DIR, container)
        print(f"├── {container}/")
        if os.path.exists(c_path):
            projects = sorted([d for d in os.listdir(c_path) if os.path.isdir(os.path.join(c_path, d))])
            for p in projects:
                p_path = os.path.join(c_path, p)
                has_ai = "✅ .ai/" if os.path.exists(os.path.join(p_path, ".ai")) else "❌ NO .ai/"
                _prd = os.path.join(p_path, "docs/product/PRD.md")
                _prd_legacy = os.path.join(p_path, "docs/PRD.md")
                has_prd = "📄 PRD.md" if (os.path.isfile(_prd) or os.path.isfile(_prd_legacy)) else "🚧 No PRD"
                print(f"│   └── {p:<25} {has_ai} | {has_prd}")
    print("")

def render_health_metrics():
    print("📊 ANTIFRAGILE HEALTH & STRESS VIEW")
    # Mock data for demonstration, should pull from real logs in prod
    print(f"→ Healing Bot Success Rate: 92%  |  Chaos Recovery: 96%")
    print(f"→ Active Repair Branches: 0      |  System Stress: 12/100")
    print("")

def render_omega_ledger():
    print("🛡️ OMEGA GATE & GOVERNANCE LEDGER")
    logs = get_last_n_logs(5)
    print(f"{'TIMESTAMP':<20} | {'ACTION / COMMAND':<25} | {'HASH / STATUS':<12}")
    print("-" * 65)
    for entry in logs:
        ts = entry.get('timestamp', '')[:19].replace("T", " ")
        action = entry.get('action') or entry.get('command') or entry.get('input', 'Unknown')
        h = entry.get('reasoning_hash', entry.get('status', 'N/A'))[:12]
        print(f"{ts:<20} | {action:<25} | {h:<12}")
    print("")

def render_learning_view():
    print("🧠 RECURSIVE LEARNING & MEMORY")
    skills = os.listdir(SKILL_DIR) if os.path.exists(SKILL_DIR) else []
    print(f"→ Total Validated Skill Manifests: {len(skills)}")
    if skills:
        print(f"→ Latest: {skills[-1]}")
    print("")

def main():
    print("=" * 65)
    print(f"  AIWF DASHBOARD v2.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    print("=" * 65)
    print("")
    
    render_structure_map()
    render_health_metrics()
    render_omega_ledger()
    render_learning_view()
    
    print("=" * 65)
    print("Suggested: `/heal check`, `/master learn`, `/dashboard v2 --live`")

if __name__ == "__main__":
    main()
