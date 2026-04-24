import os
import json

LIBRARY_DIR = 'factory/library'
REGISTRY_DIR = '.ai/registry'

def sync_registry():
    taxonomy = {"categories": {}}
    agents = {"agents": []}
    skills = {"skills": []}

    for root, dirs, files in os.walk(LIBRARY_DIR):
        for f in files:
            p = os.path.join(root, f)
            if f in ['AGENT.md', 'SKILL.md']:
                # Extract meta JSON
                meta_json = {}
                meta_p = p.replace('.md', '.meta.json')
                if os.path.exists(meta_p):
                    with open(meta_p, 'r') as mf:
                        try:
                            meta_json = json.load(mf)
                        except json.JSONDecodeError:
                            pass 

                # Populate taxonomy
                rel_path = os.path.relpath(root, LIBRARY_DIR)
                parts = rel_path.split(os.sep)
                if len(parts) >= 1:
                    cat = parts[0]
                    if cat not in taxonomy["categories"]:
                        taxonomy["categories"][cat] = []
                    taxonomy["categories"][cat].append(p)

                # Populate agents and skills
                if f == 'AGENT.md':
                    agents["agents"].append({"path": p, "meta": meta_json, "status": "active"})
                elif f == 'SKILL.md':
                    skills["skills"].append({"path": p, "meta": meta_json, "status": "active"})

    os.makedirs(REGISTRY_DIR, exist_ok=True)

    with open(os.path.join(LIBRARY_DIR, '_taxonomy.json'), 'w') as f:
        json.dump(taxonomy, f, indent=2, sort_keys=True)

    with open(os.path.join(REGISTRY_DIR, 'agents.registry.json'), 'w') as f:
        json.dump(agents, f, indent=2, sort_keys=True)

    with open(os.path.join(REGISTRY_DIR, 'skills.registry.json'), 'w') as f:
        json.dump(skills, f, indent=2, sort_keys=True)

    print(f"Taxonomy and Registries synced. Found {len(agents['agents'])} agents and {len(skills['skills'])} skills.")

if __name__ == '__main__':
    sync_registry()
