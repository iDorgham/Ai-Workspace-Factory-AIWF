#!/usr/bin/env python3
import os
import re
import subprocess
import argparse
from datetime import datetime

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_version(file_path, version_pattern, new_version):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r') as f:
        content = f.read()
    new_content = re.sub(version_pattern, new_version, content)
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Silent Phase Release Automation")
    parser.add_argument("--version-up", action="store_true")
    parser.add_argument("--tag-git", action="store_true")
    args = parser.parse_args()

    # Detect current version from AGENTS.md
    agents_path = "AGENTS.md"
    current_version = "7.1.0"
    if os.path.exists(agents_path):
        with open(agents_path, 'r') as f:
            match = re.search(r"v(\d+\.\d+\.\d+)", f.read())
            if match:
                current_version = match.group(1)

    # Increment patch version
    major, minor, patch = map(int, current_version.split('.'))
    new_version = f"{major}.{minor}.{patch + 1}"

    if args.version_up:
        # Update AGENTS.md
        update_version(agents_path, r"v\d+\.\d+\.\d+", f"v{new_version}")
        # Update last updated timestamp
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+02:00")
        update_version(agents_path, r"\*Last updated: .* \*", f"*Last updated: {now}*")

    if args.tag_git:
        run_cmd(f"git add {agents_path}")
        run_cmd(f"git commit -m 'Release v{new_version} [SILENT]'")
        run_cmd(f"git tag -a v{new_version} -m 'Phase completion v{new_version}'")

if __name__ == "__main__":
    main()
