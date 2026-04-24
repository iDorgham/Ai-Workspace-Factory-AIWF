#!/usr/bin/env python3
import json
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "memory" / "workspace-index.json"
SUGGESTIONS_FILE = ROOT / "dashboard" / "brainstorm-suggestions.md"

def check_triggers():
    if not INDEX_FILE.exists(): return []
    
    index = json.loads(INDEX_FILE.read_text())
    metrics = index.get("metrics", {})
    suggestions = []

    # Trigger 1: Cross-Workspace Pattern (FR-4.2)
    if metrics.get("total_projects", 0) >= 1:
        suggestions.append({
            "id": f"BS-{datetime.datetime.now().strftime('%s')}",
            "type": "Cross-Workspace",
            "title": "Industrial Template Synchronization",
            "description": "Detected new sovereign project structure. Recommend shared 'Common' library for cross-client assets.",
            "impact": "High",
            "trigger": "First project scaffolding detected"
        })

    # Trigger 2: Gap Detection (Example)
    if metrics.get("total_clients", 0) > 0 and metrics.get("total_projects", 0) < 2:
        suggestions.append({
            "id": f"BS-GAP-{datetime.datetime.now().strftime('%s')}",
            "type": "Gap Detection",
            "title": "Standardized Client Onboarding",
            "description": "Only 1 project for active client. Suggest generating a 'Client Playbook' to accelerate Phase 2.",
            "impact": "Medium",
            "trigger": "Low project-to-client ratio"
        })

    return suggestions[:2] # FR-4.1: Max 2 suggestions

def render_suggestions(suggestions):
    if not suggestions: return
    
    Path(SUGGESTIONS_FILE.parent).mkdir(parents=True, exist_ok=True)
    
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
