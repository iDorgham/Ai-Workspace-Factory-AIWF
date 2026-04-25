#!/usr/bin/env python3
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"

def generate_changelog():
    print("📝 Generating Industrial Changelog...")
    
    try:
        # Get commits since last tag
        last_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], text=True).strip()
        commits = subprocess.check_output(["git", "log", f"{last_tag}..HEAD", "--oneline"], text=True).splitlines()
    except:
        # Fallback to all commits if no tag exists
        commits = subprocess.check_output(["git", "log", "--oneline", "-n", "20"], text=True).splitlines()
    
    content = [
        f"# AIWF Industrial Changelog - {datetime.date.today().isoformat()}",
        "\n## 🚀 New Features & Fixes\n"
    ]
    
    for commit in commits:
        content.append(f"- {commit}")
    
    with open(CHANGELOG_FILE, "w") as f:
        f.write("\n".join(content))
    
    print(f"✅ Changelog generated at {CHANGELOG_FILE.name}")

if __name__ == "__main__":
    generate_changelog()
