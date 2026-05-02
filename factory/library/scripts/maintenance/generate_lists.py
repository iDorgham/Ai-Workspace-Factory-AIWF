import os
import json

LIBRARY_DIR = 'factory/library'

# Phase 1 & 2 Generate
rm_commands = []
mv_commands = []
with open('/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/audit_report.json', 'r') as f:
    data = json.load(f)

# Sort dead weights, pick the shallowest 33 to kill
deletes = sorted([x for x in data['dead_weights']], key=lambda k: k['lines'])[:33]
for d in deletes:
    # include meta.json
    path = d['path']
    rm_commands.append(f"rm '{path}'")
    rm_commands.append(f"rm '{path.replace('.md', '.meta.json')}'")

with open('cleanup_lists.txt', 'w') as f:
    f.write("# Phase 1: RM Commands\n")
    f.write("\n".join(rm_commands))
    f.write("\n\n# Phase 2: MV Commands\n")
    # For taxonomies... we can just assume moving seo into 07-visibility-optimization/seo if not already there
    f.write("mv 'factory/library/_legacy_pillars/02-web-platforms/seo' 'factory/library/07-visibility-optimization/seo-technical' 2>/dev/null || true\n")
