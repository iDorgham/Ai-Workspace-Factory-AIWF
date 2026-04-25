#!/usr/bin/env python3
import json
import datetime
import os
from pathlib import Path

# Try to import REPO_ROOT, fallback to discovery
try:
    from paths import REPO_ROOT
except ImportError:
    REPO_ROOT = Path(__file__).resolve().parents[4] # Adjust based on deep path

SUGGESTIONS_FILE = REPO_ROOT / ".ai" / "dashboard" / "brainstorm_suggestions.md"
MANIFEST_FILE = REPO_ROOT / ".ai" / "plan" / "_manifest.yaml"
EVOLUTION_LEDGER = REPO_ROOT / ".ai" / "logs" / "ledgers" / "evolution_ledger.jsonl"

def get_ledger_events(type_filter=None):
    if not EVOLUTION_LEDGER.exists(): return []
    events = []
    with open(EVOLUTION_LEDGER, "r") as f:
        for line in f:
            try:
                evt = json.loads(line)
                if not type_filter or evt.get("type") == type_filter:
                    events.append(evt)
            except: continue
    return events

def check_triggers():
    suggestions = []
    
    # 1. Phase Gap Detection (F5)
    if MANIFEST_FILE.exists():
        try:
            # Simple line-based YAML parser for the manifest
            phases = []
            current_phase = {}
            with open(MANIFEST_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("- id:"):
                        if current_phase: phases.append(current_phase)
                        current_phase = {"id": line.split(":")[1].strip()}
                    elif ":" in line and current_phase:
                        key, val = line.split(":", 1)
                        current_phase[key.strip()] = val.strip().strip('"')
                if current_phase: phases.append(current_phase)
            
            for phase in phases:
                if phase.get("status") in ["active", "pending", "draft"]:
                     # Check spec density (conceptual check)
                     # Path in manifest is relative to .ai/
                     spec_dir = REPO_ROOT / ".ai" / phase.get("path", "")
                     spec_count = len(list(spec_dir.glob("*.spec.json"))) if spec_dir.exists() else 0
                     if spec_count < 5:
                         suggestions.append({
                             "id": f"BS-GAP-{phase['id']}",
                             "type": "Spec Density",
                             "title": f"Low Spec Density in Phase {phase['id']}",
                             "description": f"Phase '{phase.get('name')}' has only {spec_count} specs. Recommend reaching the SDD gate (5 specs) before execution.",
                             "impact": "High",
                             "trigger": "SDD Gate Violation"
                         })
        except Exception as e:
            print(f"⚠️ Error parsing manifest: {e}")

    # 2. Mirror Drift Trend (F1 integration)
    drift_events = get_ledger_events("mirror_drift")
    if drift_events:
        last_drift = drift_events[-1]
        if last_drift.get("status") == "fail":
            suggestions.append({
                "id": f"BS-DRIFT-{datetime.datetime.now().strftime('%s')}",
                "type": "Reliability",
                "title": "Systemic Mirror Drift detected",
                "description": f"Registry drift ({last_drift.get('node_count_delta')} nodes) detected. Run /git sync to restore symmetry.",
                "impact": "Medium",
                "trigger": "Mirror Drift Failure"
            })

    # 3. Agent Utilization (Conceptual)
    # Could scan intelligence_ledger.jsonl for agent_call events
    
    return suggestions[:5] # Expanded from 2 to 5 for F5

def render_suggestions(suggestions):
    if not suggestions: return
    
    SUGGESTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    content = ["# 💡 Brainstorm Suggestions\n", f"> Last updated: {datetime.datetime.now().isoformat()}\n"]
    
    for s in suggestions:
        content.append(f"### [{s['type']}] {s['title']}")
        content.append(f"- **ID:** `{s['id']}`")
        content.append(f"- **Trigger:** {s['trigger']}")
        content.append(f"- **Impact:** {s['impact']}")
        content.append(f"- **Suggestion:** {s['description']}\n")
        content.append(f"**Action:** `/brainstorm accept {s['id']}` | `/brainstorm dismiss {s['id']}`\n")
        content.append("---")
    
    SUGGESTIONS_FILE.write_text("\n".join(content))
    print(f"✅ Generated {len(suggestions)} suggestions in {SUGGESTIONS_FILE.name}")

if __name__ == "__main__":
    found = check_triggers()
    render_suggestions(found)
