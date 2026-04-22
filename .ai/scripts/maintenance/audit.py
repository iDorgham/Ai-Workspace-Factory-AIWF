import os
import json

LIBRARY_DIR = 'factory/library'

def audit():
    dead_weights = []
    hollow_agents = []
    thin_verticals = []
    for root, dirs, files in os.walk(LIBRARY_DIR):
        # Look for agents and skills
        for f in files:
            path = os.path.join(root, f)
            if f == 'SKILL.md':
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.readlines()
                    lines = len([l for l in content if l.strip()])
                    if lines < 50:
                        dead_weights.append({'path': path, 'lines': lines, 'type': 'skill'})
            elif f == 'AGENT.md':
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.readlines()
                    lines = len([l for l in content if l.strip()])
                    if lines < 100:
                        hollow_agents.append({'path': path, 'lines': lines, 'type': 'agent'})

    with open('audit_report.json', 'w') as out:
        json.dump({'dead_weights': dead_weights, 'hollow_agents': hollow_agents}, out, indent=2)

if __name__ == '__main__':
    audit()
