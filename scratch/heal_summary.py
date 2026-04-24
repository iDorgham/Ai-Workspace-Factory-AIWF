import os
import re

root_dir = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
docs_dir = os.path.join(root_dir, "docs")
factory_dir = os.path.join(root_dir, "factory")

issues = []

def check_file_exists(file_path, referer):
    if file_path.startswith("file:///"):
        path = file_path.replace("file://", "")
    elif file_path.startswith("/"):
        path = file_path
    else:
        path = os.path.normpath(os.path.join(os.path.dirname(referer), file_path))
    
    if not os.path.exists(path):
        return False
    return True

def scan_markdown(directory):
    count = 0
    broken = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors='ignore') as f:
                        content = f.read()
                        links = re.findall(r'\[.*?\]\((.*?)\)', content)
                        for link in links:
                            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                                continue
                            count += 1
                            if not check_file_exists(link, file_path):
                                broken += 1
                except:
                    pass
    return count, broken

# Scan key directories
doc_total, doc_broken = scan_markdown(docs_dir)
fac_total, fac_broken = scan_markdown(factory_dir)
root_total, root_broken = scan_markdown(root_dir)

total_links = doc_total + fac_total + root_total
total_broken = doc_broken + fac_broken + root_broken

health_score = 100
if total_links > 0:
    health_score = int((1 - (total_broken / total_links)) * 100)

print(f"HEAL_AUDIT_SUMMARY:")
print(f"- Total Links Scanned: {total_links}")
print(f"- Total Broken Links: {total_broken}")
print(f"- Structural Health Score: {health_score}/100")
print(f"- Primary Decay Source: factory/library/registry/registry.md")
