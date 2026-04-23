import json
import os
from datetime import datetime

AGENT_FILES = [
    "factory/library/agents/05-verticals/cybersecurity-ops/cybersecurity-expert/agent.meta.json",
    "factory/library/agents/05-verticals/wealth-fintech/wealth-fintech-expert/agent.meta.json",
    "factory/library/agents/05-verticals/tourism-travel/tourism-travel-expert/agent.meta.json",
    "factory/library/agents/05-verticals/logistics-transport/logistics-transport-expert/agent.meta.json",
    "factory/library/agents/05-verticals/ecommerce-logistics/ecommerce-logistics-expert/agent.meta.json",
    "factory/library/agents/05-verticals/ai-enterprise/ai-enterprise-expert/agent.meta.json",
    "factory/library/agents/05-verticals/telecom-digital/telecom-digital-expert/agent.meta.json",
    "factory/library/agents/05-verticals/construction-proptech/construction-proptech-expert/agent.meta.json",
]

SKILL_FILES = [
    "factory/library/skills/05-verticals/islamic-finance-compliance/skill.meta.json",
    "factory/library/skills/05-verticals/mena-cultural-business-practices/skill.meta.json",
    "factory/library/skills/05-verticals/mena-regulatory-compliance/skill.meta.json",
    "factory/library/skills/05-verticals/mena-localization-payments/skill.meta.json",
    "factory/library/skills/05-verticals/mena-data-sovereignty/skill.meta.json",
]

now = datetime.utcnow().isoformat() + "Z"

def fix_agent(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    data.update({
        "name": data.get("id"),
        "version": "1.0.0",
        "source": "manual",
        "source_path": path.replace(".meta.json", "/AGENT.md"),
        "tags": [data.get("cluster"), data.get("field")],
        "dependencies": [],
        "compatibility": ["generic"],
        "quality_status": "draft",
        "last_synced_at": now
    })
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fixed {path}")

def fix_skill(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    data.update({
        "version": "1.0.0",
        "source": "manual",
        "source_path": path.replace(".meta.json", "/SKILL.md"),
        "tags": [data.get("cluster", "05-verticals"), data.get("field", os.path.basename(os.path.dirname(path)))],
        "dependencies": [],
        "compatibility": ["generic"],
        "quality_status": "draft",
        "last_synced_at": now
    })
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fixed {path}")

for f in AGENT_FILES: fix_agent(f)
for f in SKILL_FILES: fix_skill(f)
