import os
import re

root_dir = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
docs_dir = os.path.join(root_dir, "docs")
ai_dir = os.path.join(root_dir, ".ai")

issues = []

def check_file_exists(file_path, referer):
    # Handle file:/// absolute paths or relative paths
    if file_path.startswith("file:///"):
        path = file_path.replace("file://", "")
    else:
        path = os.path.abspath(os.path.join(os.path.dirname(referer), file_path))
    
    if not os.path.exists(path):
        issues.append(f"Broken Link: '{file_path}' referenced in '{referer}'")

def scan_markdown(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", errors='ignore') as f:
                    content = f.read()
                    # Find markdown links: [text](link)
                    links = re.findall(r'\[.*?\]\((.*?)\)', content)
                    for link in links:
                        if link.startswith("http") or link.startswith("#"):
                            continue
                        check_file_exists(link, file_path)

# 1. Scan for broken links
scan_markdown(docs_dir)
scan_markdown(root_dir) # Top level files like README, AGENTS

# 2. Check for required directories
required_dirs = [".ai", "docs", "factory", "workspaces", ".ai/agents", ".ai/commands", ".ai/skills"]
for d in required_dirs:
    if not os.path.isdir(os.path.join(root_dir, d)):
        issues.append(f"Missing Required Directory: '{d}'")

# Output results
if not issues:
    print("HEAL_RESULT: 100/100 EQUILIBRIUM. No structural decay detected.")
else:
    print(f"HEAL_RESULT: {100 - len(issues)}/100. Issues detected:")
    for issue in issues:
        print(f"- {issue}")
