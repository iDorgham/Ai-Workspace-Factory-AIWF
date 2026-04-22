import os
import json

LIBRARY_DIR = 'factory/library'

def analyze():
    skills_to_delete = []
    skills_to_merge = []
    agents_to_improve = []
    skills_to_improve = []

    for root, dirs, files in os.walk(LIBRARY_DIR):
        for f in files:
            path = os.path.join(root, f)
            if f == 'SKILL.md':
                with open(path, 'r', encoding='utf-8') as file:
                    lines = len([l for l in file.readlines() if l.strip()])
                    # Very small files are delete / merge
                    if lines < 15:
                        skills_to_delete.append(path)
                    elif lines < 50:
                        # Some are candidates for merge, others for improvement
                        # For now, let's mark verticals' small skills to improve, others to merge/delete
                        if 'industry-verticals' in path:
                            agents_to_improve.append(path) # We'll improve them as skills
                        else:
                            skills_to_improve.append(path)
            elif f == 'AGENT.md':
                with open(path, 'r', encoding='utf-8') as file:
                    lines = len([l for l in file.readlines() if l.strip()])
                    if lines < 100:
                        agents_to_improve.append(path)

    print("DELETE List:", len(skills_to_delete))
    print("IMPROVE Skills:", len(skills_to_improve))
    print("IMPROVE Agents:", len(agents_to_improve))

if __name__ == '__main__':
    analyze()
